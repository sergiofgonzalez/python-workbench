"""A basic but functional MCP server implementation using FastMCP."""

import os
from typing import Any

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from requests import get
from tavily import TavilyClient

load_dotenv()

mcp = FastMCP("mcp_server")

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@mcp.tool()
def search_web(query: str) -> dict[str, Any]:
    """Search the web for information."""
    return tavily_client.search(query)


@mcp.resource("github://langchain-ai/langchain-mcp-adapters/blob/main/README.md")
def read_github_readme() -> str:
    """Resource for accessing langchain-ai/langchain-mcp-adapters/README.md file."""
    url = "https://raw.githubusercontent.com/langchain-ai/langchain-mcp-adapters/main/README.md"
    try:
        response = get(url, timeout=10)
    except Exception as e:  # noqa: BLE001
        return f"Error fetching README.md: {e}"
    else:
        return response.text


@mcp.prompt()
def prompt() -> str:
    """Prompt to analyze a langchain-ai repo file with comprehensive insights."""
    return """
    You are a helpful assistant that answers user questions about LangChain, LangGraph,
    and LangSmith.

    You can use the following tools/resources to answer user questions:
    - search_web: Search the web for information.
    - read_github_readme: Access the langchain-ai repo README.md file

    If the user asks a question that is not related to LangChain, LangGraph, or
    LangSmith, you should say "I'm sorry, but I can only answer questions related to
    LangChain, LangGraph, and LangSmith.".

    You may ask clarifying questions to the user to better understand their question.
    """


if __name__ == "__main__":
    mcp.run(transport="stdio")
