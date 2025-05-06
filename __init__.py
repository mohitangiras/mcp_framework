"""
MCP Framework - A flexible and extensible framework for building Model Context Protocol servers and clients.
"""

from .core.base_server import BaseMCPServer
from .core.base_client import BaseMCPClient
from .core.context_manager import ContextManager
from .core.nl_interface import NaturalLanguageInterface

__version__ = "0.1.0"
__all__ = [
    "BaseMCPServer",
    "BaseMCPClient",
    "ContextManager",
    "NaturalLanguageInterface"
] 