from typing import Any, Dict, List, Optional
from ..core.base_client import BaseMCPClient
import logging

class MongoDBClient(BaseMCPClient):
    """Client for interacting with the MongoDB MCP server."""
    
    def __init__(self, server_url: str):
        super().__init__("mongodb_client", server_url)
    
    async def find_documents(self, collection: str, query: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
        """Find documents in a collection."""
        try:
            response = await self.call_tool("find_documents", {
                "collection": collection,
                "query": query,
                "limit": limit
            })
            return response.get("result", [])
        except Exception as e:
            self.logger.error(f"Error finding documents: {str(e)}")
            raise
    
    async def insert_document(self, collection: str, document: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a document into a collection."""
        try:
            response = await self.call_tool("insert_document", {
                "collection": collection,
                "document": document
            })
            return response.get("result", {})
        except Exception as e:
            self.logger.error(f"Error inserting document: {str(e)}")
            raise
    
    async def update_document(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        """Update documents in a collection."""
        try:
            response = await self.call_tool("update_document", {
                "collection": collection,
                "query": query,
                "update": update
            })
            return response.get("result", {})
        except Exception as e:
            self.logger.error(f"Error updating documents: {str(e)}")
            raise
    
    async def delete_document(self, collection: str, query: Dict[str, Any]) -> Dict[str, Any]:
        """Delete documents from a collection."""
        try:
            response = await self.call_tool("delete_document", {
                "collection": collection,
                "query": query
            })
            return response.get("result", {})
        except Exception as e:
            self.logger.error(f"Error deleting documents: {str(e)}")
            raise 