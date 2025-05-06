# MCP Framework

A flexible and extensible framework for building Model Context Protocol (MCP) servers and clients in Python.

## Features

- Easy integration with any MCP server
- Natural language interface for interacting with MCP servers
- Context management and caching
- Built-in support for MongoDB (example implementation)
- Extensible architecture for adding new servers and clients
- Comprehensive logging and error handling

## Installation

```bash
pip install -r requirements.txt
```

## Project Structure

```
mcp_framework/
├── core/
│   ├── base_server.py
│   ├── base_client.py
│   ├── context_manager.py
│   └── nl_interface.py
├── servers/
│   └── mongodb_server.py
├── clients/
│   └── mongodb_client.py
├── utils/
├── docs/
└── requirements.txt
```

## Quick Start

### Creating a New MCP Server

```python
from mcp_framework.core.base_server import BaseMCPServer

class MyCustomServer(BaseMCPServer):
    def __init__(self):
        super().__init__("my_server", "Description of my server")
        self._register_tools()
    
    def _register_tools(self):
        self.register_tool(
            name="my_tool",
            description="Description of my tool",
            func=self.my_tool
        )
    
    async def my_tool(self, param1: str, param2: int):
        # Implement your tool logic here
        pass
```

### Creating a New MCP Client

```python
from mcp_framework.core.base_client import BaseMCPClient

class MyCustomClient(BaseMCPClient):
    def __init__(self, server_url: str):
        super().__init__("my_client", server_url)
    
    async def call_my_tool(self, param1: str, param2: int):
        response = await self.call_tool("my_tool", {
            "param1": param1,
            "param2": param2
        })
        return response.get("result")
```

### Using the Natural Language Interface

```python
from mcp_framework.core.nl_interface import NaturalLanguageInterface

nl_interface = NaturalLanguageInterface(openai_api_key="your-api-key")
result = await nl_interface.process_query(
    "Find all users with age greater than 30",
    available_tools=[...]
)
```

### Using the Context Manager

```python
from mcp_framework.core.context_manager import ContextManager

context_manager = ContextManager()
context_manager.set_context("user_id", "123", ttl=3600)
user_id = context_manager.get_context("user_id")
```

## Example: MongoDB Integration

### Starting the MongoDB Server

```python
from mcp_framework.servers.mongodb_server import MongoDBServer

server = MongoDBServer(
    connection_string="mongodb://localhost:27017",
    database_name="my_database"
)
await server.start()
```

### Using the MongoDB Client

```python
from mcp_framework.clients.mongodb_client import MongoDBClient

client = MongoDBClient("http://localhost:8000")
await client.connect()

# Find documents
documents = await client.find_documents(
    collection="users",
    query={"age": {"$gt": 30}},
    limit=10
)

# Insert document
result = await client.insert_document(
    collection="users",
    document={"name": "John", "age": 35}
)
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Add your changes
4. Submit a pull request

## License

MIT License

## Documentation

For more detailed documentation, please refer to the `docs/` directory. 