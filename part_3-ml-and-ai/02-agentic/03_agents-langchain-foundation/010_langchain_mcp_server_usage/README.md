# 010: Configuring a LangChain Agent to use other people's MCP servers
> Illustrates how to use other people's mcp servers

## Project description

This project illustrates how to wire your agent to use other people's MCP servers, like the ones you will find in the Internet.

### Lab 1: Configuring your agent to use a Time MCP server

[Time MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/time) is an MCP server that provides time and timezone conversion capabilities.

The server enables LLMs to get current time information and perform timezone conversions using IANA timezone names with automatic TZ detection.

The MCP server provides two tools:

+ `get_current_time`: get current time in a specific TZ or system TZ.

    Requires `timezone` (str): IANA timezone name (e.g., "America/New_York", "Europe/London")

+ `convert_time`: convert time between TZs

    Arguments:
        - `source_timezone` (str): Source IANA TZ
        - `time` (str): Time in 24-hr format (HH:MM)
        - `target_timezone` (str): Target IANA TZ

Server Config from the website is as follows:

```json
{
  "mcpServers": {
    "time": {
      "command": "uvx",
      "args": [
        "mcp-server-time",
        "--local-timezone=Europe/Madrid"
      ]
    }
  }
}
```

Create an MCP Server (MultiServerMCPClient) that uses that MCP server and wire it to an agent.

Test the agent using a prompt such as "What time is it?" and "What time is it in New York?".

### Lab 2: Configuring your agent to use Kiwi Travel MCP

The [Kiwi Travel MCP](https://mcp.so/server/kiwi-travel-mcp/Vytautas%20Dargis) integrates flight search capabilities directly into AI conversations, allowing users to search and book flights seamlessly through AI agents.

The server config looks as follows:

```json
{
  "mcpServers": {
    "kiwi-com-flight-search": {
      "url": "https://mcp.kiwi.com"
    }
  }
}
```


## Running the program

You can run the application with:

```bash
uv run python main.py
```

## Project management

This project is managed using `uv`.
