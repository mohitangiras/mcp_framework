from typing import Any, Dict, Optional
from cachetools import TTLCache
import json
import logging
from datetime import datetime

class ContextManager:
    """Manages context and caching for MCP framework."""
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.cache = TTLCache(maxsize=max_size, ttl=ttl)
        self.context_store = {}
        self.logger = logging.getLogger("mcp.context_manager")
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def set_context(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set a context value with optional TTL."""
        try:
            if ttl:
                self.cache[key] = value
            else:
                self.context_store[key] = {
                    "value": value,
                    "timestamp": datetime.now().isoformat()
                }
            self.logger.debug(f"Set context for key: {key}")
        except Exception as e:
            self.logger.error(f"Error setting context: {str(e)}")
            raise
    
    def get_context(self, key: str) -> Optional[Any]:
        """Get a context value."""
        try:
            # First check cache
            if key in self.cache:
                return self.cache[key]
            
            # Then check context store
            if key in self.context_store:
                return self.context_store[key]["value"]
            
            return None
        except Exception as e:
            self.logger.error(f"Error getting context: {str(e)}")
            return None
    
    def clear_context(self, key: str):
        """Clear a specific context value."""
        try:
            if key in self.cache:
                del self.cache[key]
            if key in self.context_store:
                del self.context_store[key]
            self.logger.debug(f"Cleared context for key: {key}")
        except Exception as e:
            self.logger.error(f"Error clearing context: {str(e)}")
            raise
    
    def clear_all_context(self):
        """Clear all context values."""
        try:
            self.cache.clear()
            self.context_store.clear()
            self.logger.debug("Cleared all context")
        except Exception as e:
            self.logger.error(f"Error clearing all context: {str(e)}")
            raise
    
    def get_all_context(self) -> Dict[str, Any]:
        """Get all context values."""
        return {
            "cache": dict(self.cache),
            "context_store": self.context_store
        }
    
    def share_context(self, source_key: str, target_key: str):
        """Share context between different parts of the system."""
        try:
            value = self.get_context(source_key)
            if value is not None:
                self.set_context(target_key, value)
                self.logger.debug(f"Shared context from {source_key} to {target_key}")
        except Exception as e:
            self.logger.error(f"Error sharing context: {str(e)}")
            raise 