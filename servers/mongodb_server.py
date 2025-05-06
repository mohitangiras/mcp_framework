from typing import Any, Dict, List, Optional
from pymongo import MongoClient
from ..core.base_server import BaseMCPServer
import logging

class MongoDBServer(BaseMCPServer):
    """MCP server for MongoDB interactions."""
    
    def __init__(self, connection_string: str, database_name: str):
        super().__init__("mongodb", "MCP server for MongoDB interactions")
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self._register_tools()
    
    def _register_tools(self):
        """Register MongoDB-specific tools."""
        self.register_tool(
            name="find_documents",
            description="Find documents in a MongoDB collection",
            func=self.find_documents
        )
        
        self.register_tool(
            name="insert_document",
            description="Insert a document into a MongoDB collection",
            func=self.insert_document
        )
        
        self.register_tool(
            name="update_document",
            description="Update documents in a MongoDB collection",
            func=self.update_document
        )
        
        self.register_tool(
            name="delete_document",
            description="Delete documents from a MongoDB collection",
            func=self.delete_document
        )
    
    async def find_documents(self, collection: str, query: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
        """Find documents in a collection."""
        try:
            cursor = self.db[collection].find(query).limit(limit)
            return list(cursor)
        except Exception as e:
            self.logger.error(f"Error finding documents: {str(e)}")
            raise
    
    async def insert_document(self, collection: str, document: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a document into a collection."""
        try:
            result = self.db[collection].insert_one(document)
            return {"inserted_id": str(result.inserted_id)}
        except Exception as e:
            self.logger.error(f"Error inserting document: {str(e)}")
            raise
    
    async def update_document(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        """Update documents in a collection."""
        try:
            result = self.db[collection].update_many(query, {"$set": update})
            return {
                "matched_count": result.matched_count,
                "modified_count": result.modified_count
            }
        except Exception as e:
            self.logger.error(f"Error updating documents: {str(e)}")
            raise
    
    async def delete_document(self, collection: str, query: Dict[str, Any]) -> Dict[str, Any]:
        """Delete documents from a collection."""
        try:
            result = self.db[collection].delete_many(query)
            return {"deleted_count": result.deleted_count}
        except Exception as e:
            self.logger.error(f"Error deleting documents: {str(e)}")
            raise 