import streamlit as st
import asyncio
from mcp_framework.clients.mongodb_client import MongoDBClient
from mcp_framework.core.context_manager import ContextManager
from mcp_framework.core.nl_interface import NaturalLanguageInterface
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize context manager
context_manager = ContextManager()

# Initialize natural language interface
nl_interface = NaturalLanguageInterface(openai_api_key=os.getenv("OPENAI_API_KEY"))

# Initialize clients
mongo_client = MongoDBClient("http://localhost:8000")
postgres_client = None  # Will be initialized when needed

async def init_clients():
    """Initialize MCP clients."""
    await mongo_client.connect()
    # Add postgres client initialization when needed

def main():
    st.title("MCP Framework Demo")
    st.write("Interact with MongoDB and PostgreSQL using natural language")
    
    # Initialize clients
    asyncio.run(init_clients())
    
    # Sidebar for database selection
    db_type = st.sidebar.selectbox(
        "Select Database",
        ["MongoDB", "PostgreSQL"]
    )
    
    # Natural language input
    query = st.text_area("Enter your query in natural language", height=100)
    
    if st.button("Execute"):
        if query:
            with st.spinner("Processing..."):
                # Get available tools based on selected database
                if db_type == "MongoDB":
                    available_tools = [
                        {
                            "name": "aggregate",
                            "description": "Execute MongoDB aggregation pipelines",
                            "parameters": {
                                "collection": "string",
                                "pipeline": "array",
                                "options": "object"
                            }
                        },
                        {
                            "name": "explain",
                            "description": "Get execution plans for aggregation pipelines",
                            "parameters": {
                                "collection": "string",
                                "pipeline": "array",
                                "verbosity": "string"
                            }
                        }
                    ]
                else:
                    available_tools = [
                        {
                            "name": "execute_query",
                            "description": "Execute a SQL query on PostgreSQL",
                            "parameters": {
                                "query": "string",
                                "params": "object"
                            }
                        },
                        {
                            "name": "create_table",
                            "description": "Create a new table in PostgreSQL",
                            "parameters": {
                                "table_name": "string",
                                "columns": "object"
                            }
                        }
                    ]
                
                # Process the query
                result = asyncio.run(nl_interface.process_query(query, available_tools))
                
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    st.write("Tool Selection:", result)
                    
                    # Execute the selected tool
                    try:
                        if db_type == "MongoDB":
                            tool_response = asyncio.run(
                                mongo_client.call_tool(
                                    result["tool_name"],
                                    result["parameters"]
                                )
                            )
                        else:
                            tool_response = asyncio.run(
                                postgres_client.call_tool(
                                    result["tool_name"],
                                    result["parameters"]
                                )
                            )
                        
                        st.write("Result:", json.dumps(tool_response, indent=2))
                    except Exception as e:
                        st.error(f"Error executing tool: {str(e)}")

if __name__ == "__main__":
    main() 