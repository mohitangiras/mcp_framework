from typing import Any, Dict, List, Optional
import asyncpg
from mcp_framework.core.base_server import BaseMCPServer
import logging

class PostgresServer(BaseMCPServer):
    """MCP server for PostgreSQL interactions."""
    
    def __init__(self, connection_string: str):
        super().__init__("postgres", "MCP server for PostgreSQL interactions")
        self.connection_string = connection_string
        self.pool = None
        self._register_tools()
    
    async def _get_pool(self):
        """Get or create connection pool."""
        if not self.pool:
            self.pool = await asyncpg.create_pool(self.connection_string)
        return self.pool
    
    def _register_tools(self):
        """Register PostgreSQL-specific tools."""
        self.register_tool(
            name="execute_query",
            description="Execute a SQL query on PostgreSQL",
            func=self.execute_query
        )
        
        self.register_tool(
            name="create_table",
            description="Create a new table in PostgreSQL",
            func=self.create_table
        )
        
        self.register_tool(
            name="insert_data",
            description="Insert data into a PostgreSQL table",
            func=self.insert_data
        )
    
    async def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a SQL query."""
        try:
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                if params:
                    result = await conn.fetch(query, **params)
                else:
                    result = await conn.fetch(query)
                return [dict(row) for row in result]
        except Exception as e:
            self.logger.error(f"Error executing query: {str(e)}")
            raise
    
    async def create_table(self, table_name: str, columns: Dict[str, str]) -> Dict[str, Any]:
        """Create a new table."""
        try:
            columns_def = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"
            
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                await conn.execute(query)
                return {"status": "success", "message": f"Table {table_name} created successfully"}
        except Exception as e:
            self.logger.error(f"Error creating table: {str(e)}")
            raise
    
    async def insert_data(self, table_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert data into a table."""
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join([f"${i+1}" for i in range(len(data))])
            values = list(data.values())
            
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) RETURNING *"
            
            pool = await self._get_pool()
            async with pool.acquire() as conn:
                result = await conn.fetchrow(query, *values)
                return dict(result)
        except Exception as e:
            self.logger.error(f"Error inserting data: {str(e)}")
            raise 