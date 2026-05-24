"""Illustrates how to use other people's mcp servers."""

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
        "time": {
            "transport": "stdio",
            "command": "uvx",
            "args": [
                "mcp-server-time",
                "--local-timezone=Europe/Madrid",
            ],
        },
        # Lab 2
        "travel_server": {
            "transport": "streamable_http",
            "url": "https://mcp.kiwi.com",
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
    tools = await client.get_tools()
    for tool in tools:
        print(f"Tool name: {tool.name}")
        print(f"Tool description: {tool.description}")
        print(f"Tool args schema: {tool.args_schema}")
        print()
    print("=" * 80)

    agent = create_agent(
        llm,
        tools=tools,
    )

    question = HumanMessage("What time is it?")
    response = await agent.ainvoke({"messages": [question]})
    rich.print(response)
    print("=" * 80)

    question = HumanMessage("What time is it in NewYork")
    response = await agent.ainvoke({"messages": [question]})
    rich.print(response)
    print("=" * 80)

    # Lab 2
    sys_prompt = "You are a travel agent. No follow up questions."

    agent = create_agent(
        llm,
        tools=tools,
        system_prompt=sys_prompt,
        checkpointer=InMemorySaver(),
    )

    config = ensure_config({"configurable": {"thread_id": "1"}})
    question = HumanMessage(
        "Get me a direct flight from Madrid to Leon, Spain on May 29 2026",
    )
    response = await agent.ainvoke({"messages": [question]}, config=config)
    rich.print(response)
    print("=" * 80)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
