
import os
from mcp_framework.examples.streamlit_app.servers.postgres_server import PostgresServer
from fastapi import FastAPI

app = FastAPI()
server = PostgresServer(
    connection_string=os.getenv("POSTGRES_URI", "postgresql://localhost:5432/mcp_demo")
)
app.include_router(server.mcp.router)
