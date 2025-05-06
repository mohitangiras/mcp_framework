# MCP Framework Example Application

This example demonstrates how to use the MCP Framework with MongoDB and PostgreSQL databases through a Streamlit interface. The MongoDB integration uses the official MongoDB MCP server from [mongodb-developer/mongodb-mcp-server](https://github.com/mongodb-developer/mongodb-mcp-server).

## Prerequisites

- Python 3.8+
- Node.js 16+ and npm 8+
- MongoDB running locally or accessible via URI
- PostgreSQL running locally or accessible via URI
- OpenAI API key

## Setup

1. Install Node.js and npm:
   - **macOS** (using Homebrew):
     ```bash
     brew install node
     ```
   - **Linux** (Ubuntu/Debian):
     ```bash
     curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
     sudo apt-get install -y nodejs
     ```
   - **Windows**:
     Download and install from [Node.js official website](https://nodejs.org/)

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install MongoDB MCP server:
   ```bash
   npm install -g @pash1986/mcp-server-mongodb
   ```

4. Create a `.env` file with the following content:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   MONGODB_URI=mongodb://localhost:27017
   MONGODB_DB=mcp_demo
   POSTGRES_URI=postgresql://localhost:5432/mcp_demo
   ```

5. Make sure MongoDB and PostgreSQL are running and accessible.

## Running the Application

To run all components (MongoDB server, PostgreSQL server, and Streamlit app):

```bash
python run.py
```

This will:
1. Start the MongoDB MCP server on port 8000
2. Start the PostgreSQL MCP server on port 8001
3. Launch the Streamlit application

## Using the Application

1. Open your browser and navigate to the Streamlit app (usually http://localhost:8501)
2. Select the database you want to interact with (MongoDB or PostgreSQL)
3. Enter your query in natural language
4. Click "Execute" to process your query

### Example Queries

MongoDB:
- "Find all users with age greater than 30"
- "Show me the execution plan for finding users by age"
- "Aggregate users by city and show average age"

PostgreSQL:
- "Create a new table called users with columns id, name, and age"
- "Execute a query to select all users from the users table"

## Architecture

The application consists of:

1. **MCP Servers**:
   - MongoDB server (port 8000) using the official MongoDB MCP server
   - PostgreSQL server (port 8001)

2. **Streamlit Interface**:
   - Natural language input
   - Database selection
   - Query execution and results display

3. **Components**:
   - Natural Language Interface for query processing
   - Context Manager for maintaining state
   - MCP Clients for database interaction

## MongoDB MCP Server Features

The MongoDB MCP server provides the following tools:

1. **aggregate**: Execute MongoDB aggregation pipelines
   - Input: collection name, pipeline stages, and options
   - Supports all MongoDB aggregation operations
   - Default limit of 1000 documents
   - 30-second timeout

2. **explain**: Get execution plans for aggregation pipelines
   - Input: collection name, pipeline stages, and verbosity level
   - Verbosity options: "queryPlanner", "executionStats", "allPlansExecution"

## Troubleshooting

1. If servers fail to start:
   - Check if MongoDB and PostgreSQL are running
   - Verify connection strings in `.env`
   - Check if ports 8000 and 8001 are available
   - Ensure Node.js and npm are installed correctly
   - Verify MongoDB MCP server installation with `npm list -g @pash1986/mcp-server-mongodb`

2. If queries fail:
   - Check the natural language query format
   - Verify database permissions
   - Check server logs for detailed error messages
   - For MongoDB issues, check the MCP server logs 