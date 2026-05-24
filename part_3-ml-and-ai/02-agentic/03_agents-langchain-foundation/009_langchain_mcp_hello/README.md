# 009: Hello, MCP and LangChain agent
> Illustrates how to create your own mcp server that is then used by a LangChain agent

## Project description

Illustrates how to create your own MCP server with FastMCP which will host tools, resources, and prompts, and then use it with a LangChain agent.

### Lab 1: Build an MCP server

Using the official [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk), build an MCP server `mcp_server.py` that provides:

- A tool to search the web, using Tavily.

- A resource, that returns the context of the README.md file hosted in `https://raw.githubusercontent.com/langchain-ai/langchain-mcp-adapters/main/README.md`.

- A prompt that instructs an agent to answer questions about LangChain, LangGraph, and LangSmith.

### Lab 2: Build an agent with an MCP client that connects to the MCP server

Using LangChain, create an async app that instantiates an MCP server.

In main, access the tools, resources, and prompts, and print their content.

After that, instantiate a langchain agent, and use the system prompt from the MCP server, and the tools from the same server. Then invoke it asynchronously using `agent.ainvoke()`.

Finally, print the result.

## Running the program

You can run the MCP server with:

```bash
uv run mcp_server.py
```

You can run the agent that uses the MCP server using:

```bash
uv run python mcp_agent.py
```

## Project management

This project is managed using `uv`. Additional libraries have been included to support MCP servers and clients:

- Server requires: "mcp>=1.27.1"
- Client requires: "langchain-mcp-adapters>=0.2.2",
