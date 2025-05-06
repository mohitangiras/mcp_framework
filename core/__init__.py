"""
Core components of the MCP Framework.
"""

from .base_server import BaseMCPServer
from .base_client import BaseMCPClient
from .context_manager import ContextManager
from .nl_interface import NaturalLanguageInterface

__all__ = [
    "BaseMCPServer",
    "BaseMCPClient",
    "ContextManager",
    "NaturalLanguageInterface"
] 