import subprocess
import os
import threading
from dotenv import load_dotenv
import uvicorn
from mcp_framework.servers.mongodb_server import MongoDBServer
from mcp_framework.examples.streamlit_app.servers.postgres_server import PostgresServer

# Load environment variables
load_dotenv()

def run_mongodb_server():
    """Run the MongoDB MCP server."""
    server = MongoDBServer(
        connection_string=os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
        database_name=os.getenv("MONGODB_DB", "mcp_demo")
    )
    server.mcp.run(transport="sse", host="localhost", port=8002)

def run_postgres_server():
    """Run the PostgreSQL MCP server."""
    server = PostgresServer(
        connection_string=os.getenv("POSTGRES_URI", "postgresql://localhost:5432/mcp_demo")
    )
    server.mcp.run(transport="sse", host="localhost", port=8003)

def run_streamlit():
    """Run the Streamlit application."""
    return subprocess.Popen([
        "streamlit",
        "run",
        os.path.join(os.path.dirname(__file__), "app.py")
    ])

if __name__ == "__main__":
    # Start MongoDB server in a thread
    mongodb_thread = threading.Thread(target=run_mongodb_server)
    mongodb_thread.daemon = True
    mongodb_thread.start()
    
    # Start PostgreSQL server in a thread
    postgres_thread = threading.Thread(target=run_postgres_server)
    postgres_thread.daemon = True
    postgres_thread.start()
    
    # Run Streamlit app in the main thread
    streamlit_process = run_streamlit()
    
    try:
        # Wait for all processes to finish
        mongodb_thread.join()
        postgres_thread.join()
        streamlit_process.wait()
    except KeyboardInterrupt:
        # Terminate all processes
        streamlit_process.terminate() 