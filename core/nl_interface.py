from typing import Any, Dict, List, Optional
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import logging
import json

class NaturalLanguageInterface:
    """Natural language interface for the MCP framework."""
    
    def __init__(self, openai_api_key: str):
        self.llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
        self.logger = logging.getLogger("mcp.nl_interface")
        self._setup_logging()
        self._setup_prompts()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def _setup_prompts(self):
        """Setup prompt templates for different tasks."""
        self.tool_selection_prompt = PromptTemplate(
            input_variables=["query", "available_tools"],
            template="""
            Given the following user query and available tools, determine which tool should be used and what parameters to pass.
            
            User Query: {query}
            Available Tools: {available_tools}
            
            Respond in JSON format with the following structure:
            {{
                "tool_name": "name of the tool to use",
                "parameters": {{
                    "param1": "value1",
                    "param2": "value2"
                }}
            }}
            """
        )
        
        self.tool_selection_chain = LLMChain(
            llm=self.llm,
            prompt=self.tool_selection_prompt
        )
    
    async def process_query(self, query: str, available_tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process a natural language query and determine which tool to use."""
        try:
            # Format available tools for the prompt
            tools_str = json.dumps(available_tools, indent=2)
            
            # Get tool selection from LLM
            response = await self.tool_selection_chain.arun(
                query=query,
                available_tools=tools_str
            )
            
            # Parse the response
            try:
                result = json.loads(response)
                return result
            except json.JSONDecodeError:
                self.logger.error(f"Failed to parse LLM response: {response}")
                return {
                    "error": "Failed to parse tool selection response"
                }
                
        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            return {
                "error": str(e)
            }
    
    def format_tool_description(self, tool: Dict[str, Any]) -> str:
        """Format a tool description for the LLM."""
        return f"""
        Name: {tool['name']}
        Description: {tool['description']}
        Parameters: {json.dumps(tool.get('parameters', {}), indent=2)}
        """ 