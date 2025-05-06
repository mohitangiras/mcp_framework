from typing import Any, Dict, Optional
from fastmcp import FastMCP
from pydantic import BaseModel
import asyncio
import logging

class BaseMCPServer:
    """Base class for all MCP servers in the framework."""
    
    def __init__(self, server_name: str, description: str):
        self.server_name = server_name
        self.description = description
        self.mcp = FastMCP(server_name)
        self.logger = logging.getLogger(f"mcp.{server_name}")
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging configuration for the server."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    async def start(self, host: str = "localhost", port: int = 8000):
        """Start the MCP server."""
        try:
            self.logger.info(f"Starting {self.server_name} MCP server on {host}:{port}")
            await self.mcp.run(host=host, port=port)
        except Exception as e:
            self.logger.error(f"Failed to start server: {str(e)}")
            raise
    
    def register_tool(self, name: str, description: str, func: callable):
        """Register a new tool with the MCP server."""
        self.mcp.tool(name=name, description=description)(func)
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming requests to the server."""
        try:
            response = await self.mcp.handle_request(request)
            return response
        except Exception as e:
            self.logger.error(f"Error handling request: {str(e)}")
            return {"error": str(e)}
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get information about the server and its capabilities."""
        return {
            "name": self.server_name,
            "description": self.description,
            "tools": self.mcp.get_tools()
        } 