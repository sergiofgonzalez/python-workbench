"""Illustrates how to create your own mcp agent that uses an MCP custom server."""

import asyncio
import os

import rich
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_core.runnables import ensure_config
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import SecretStr

load_dotenv()

client = MultiServerMCPClient(
    {
        "local_server": {
            "transport": "stdio",  # see: https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
            "command": "python",
            "args": ["mcp_server.py"],
        },
    },
)

llm = ChatOpenAI(
    model="bedrock-claude-sonnet-4-5",
    api_key=SecretStr(os.environ["LITELLM_API_KEY"]),
    base_url=os.getenv("LITELLM_BASE_URL"),
)


async def main() -> None:
    """Async application entry point."""
    # Access metadata information from the MCP server.
    tools = await client.get_tools()
    print("Tools available from the MCP server:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")

    resources = await client.get_resources("local_server")
    print("Resources available from the MCP server:")
    for resource in resources:
        rich.print(f"- {resource}")

    prompts = await client.get_prompt("local_server", "prompt")

    print("Prompt(s) from MCP server:")
    for prompt in prompts:
        print(f"- {prompt.content}")
    prompt_content = prompts[0].content if prompts else ""
    if isinstance(prompt_content, str):
        sys_prompt = prompt_content
    else:
        # while sys_prompt could be a list of messages, in this example we expect
        # it to be a string.
        msg = "Expected prompt content to be a string."
        raise TypeError(msg)
    print("=" * 80)

    # create an agent that uses the MCP server
    agent = create_agent(
        llm,
        system_prompt=sys_prompt,
        tools=tools,
        checkpointer=InMemorySaver(),
    )

    config = ensure_config({"configurable": {"thread_id": "1"}})
    question = HumanMessage("Tell me about the langchain-mcp-adapters library")

    response = await agent.ainvoke(
        {"messages": [question]},
        config=config,
    )

    rich.print("Agent response:")
    rich.print(response)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
