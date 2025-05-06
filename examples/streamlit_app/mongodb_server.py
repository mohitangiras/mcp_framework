
import os
from mcp_framework.servers.mongodb_server import MongoDBServer
from fastapi import FastAPI

app = FastAPI()
server = MongoDBServer(
    connection_string=os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
    database_name=os.getenv("MONGODB_DB", "mcp_demo")
)
app.include_router(server.mcp.router)
