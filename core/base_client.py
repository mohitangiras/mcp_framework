from typing import Any, Dict, List, Optional
import aiohttp
import logging
from pydantic import BaseModel
import json

class BaseMCPClient:
    """Base class for all MCP clients in the framework."""
    
    def __init__(self, client_name: str, server_url: str):
        self.client_name = client_name
        self.server_url = server_url
        self.logger = logging.getLogger(f"mcp.client.{client_name}")
        self._setup_logging()
        self.session = None
    
    def _setup_logging(self):
        """Setup logging configuration for the client."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    async def connect(self):
        """Establish connection with the MCP server."""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def disconnect(self):
        """Close the connection with the MCP server."""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific tool on the MCP server."""
        try:
            if not self.session:
                await self.connect()
            
            async with self.session.post(
                f"{self.server_url}/tool/{tool_name}",
                json=params
            ) as response:
                return await response.json()
        except Exception as e:
            self.logger.error(f"Error calling tool {tool_name}: {str(e)}")
            raise
    
    async def get_server_info(self) -> Dict[str, Any]:
        """Get information about the connected MCP server."""
        try:
            if not self.session:
                await self.connect()
            
            async with self.session.get(f"{self.server_url}/info") as response:
                return await response.json()
        except Exception as e:
            self.logger.error(f"Error getting server info: {str(e)}")
            raise
    
    async def list_available_tools(self) -> List[str]:
        """Get a list of available tools from the server."""
        server_info = await self.get_server_info()
        return server_info.get("tools", []) 