from typing import Any, Dict, List, Optional
import subprocess
import os
import json
import logging
from mcp_framework.core.base_server import BaseMCPServer

class MongoDBServer(BaseMCPServer):
    """MCP server for MongoDB interactions using the official MongoDB MCP server."""
    
    def __init__(self, connection_string: str, database_name: str):
        super().__init__("mongodb", "MCP server for MongoDB interactions")
        self.connection_string = connection_string
        self.database_name = database_name
        self.process = None
        self._register_tools()
    
    def _register_tools(self):
        """Register MongoDB-specific tools."""
        self.register_tool(
            name="aggregate",
            description="Execute MongoDB aggregation pipelines",
            func=self.aggregate
        )
        
        self.register_tool(
            name="explain",
            description="Get execution plans for aggregation pipelines",
            func=self.explain
        )
    
    async def start(self, host: str = "localhost", port: int = 8000):
        """Start the MongoDB MCP server."""
        try:
            # Set environment variables for the MCP server
            env = os.environ.copy()
            env["MONGODB_URI"] = self.connection_string
            
            # Start the MCP server process
            self.process = subprocess.Popen(
                ["npx", "-y", "@pash1986/mcp-server-mongodb"],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.logger.info(f"Started MongoDB MCP server on {host}:{port}")
        except Exception as e:
            self.logger.error(f"Failed to start server: {str(e)}")
            raise
    
    async def stop(self):
        """Stop the MongoDB MCP server."""
        if self.process:
            self.process.terminate()
            self.process = None
    
    async def aggregate(self, collection: str, pipeline: List[Dict[str, Any]], options: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute MongoDB aggregation pipeline."""
        try:
            request = {
                "collection": collection,
                "pipeline": pipeline,
                "options": options or {}
            }
            
            response = await self.handle_request(request)
            return response.get("result", [])
        except Exception as e:
            self.logger.error(f"Error executing aggregation: {str(e)}")
            raise
    
    async def explain(self, collection: str, pipeline: List[Dict[str, Any]], verbosity: str = "queryPlanner") -> Dict[str, Any]:
        """Get execution plan for aggregation pipeline."""
        try:
            request = {
                "collection": collection,
                "pipeline": pipeline,
                "verbosity": verbosity
            }
            
            response = await self.handle_request(request)
            return response.get("result", {})
        except Exception as e:
            self.logger.error(f"Error getting execution plan: {str(e)}")
            raise 