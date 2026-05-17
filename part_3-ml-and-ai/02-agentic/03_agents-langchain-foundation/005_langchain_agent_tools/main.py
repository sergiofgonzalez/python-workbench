"""Illustrate how to provide an agent with tools."""

import os
from typing import Any

import rich
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from tavily import TavilyClient

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def square_root(x: float) -> float:
    """Calculate the square root of a number."""
    rich.print(f"Calculating the square root of {x}...")
    return x**0.5


@tool
def web_search(query: str) -> dict[str, Any]:
    """Search the web for information on the given query."""
    return tavily_client.search(query)


def invoke_tool() -> None:
    """Illustrate how to invoke a tool."""
    try:
        square_root(16)  # ty:ignore[call-non-callable]
    except Exception as e:  # noqa: BLE001
        print(f"An error occurred: {e} (type: {type(e).__name__})")

    result = square_root.invoke({"x": 16})
    print(f"The square root of 16 is: {result}")


def agent_with_tool() -> None:
    """Illustrate how to use a tool within an agent."""
    llm = ChatOpenAI(
        model="bedrock-claude-haiku-4-5",
        api_key=SecretStr(os.environ["LITELLM_API_KEY"]),
        base_url=os.getenv("LITELLM_BASE_URL"),
    )

    system_prompt = """
    You are an arithmetic wizard. Use your tools to calculate the square root of any number.
    """  # noqa: E501

    agent = create_agent(
        llm,
        system_prompt=system_prompt,
        tools=[square_root],
    )

    question = HumanMessage("What is the square root of 467?")

    response = agent.invoke(
        {"messages": [question]},
    )

    rich.print(response["messages"][-1].content)
    print("-" * 80)

    # To see what it went under the hood, you can print the entire response:
    rich.print(response)
    print("-" * 80)

    # In particular, tool call appears in the first AI message
    rich.print(response["messages"][1].tool_calls)


def agent_with_web_search_tool() -> None:
    """Illustrate how to use a web search tool within an agent."""
    llm = ChatOpenAI(
        model="bedrock-claude-sonnet-4-5",
        api_key=SecretStr(os.environ["LITELLM_API_KEY"]),
        base_url=os.getenv("LITELLM_BASE_URL"),
    )

    # agent without web search tool displays stale information
    agent = create_agent(
        llm,
    )

    question = HumanMessage("Who is the current mayor of Leon, Spain?")

    response = agent.invoke(
        {"messages": [question]},
    )

    print("--- Answering a question without the web search tool ---")
    rich.print(response["messages"][-1].content)
    print("-" * 80)

    # agent with web search tool displays up to date information
    agent = create_agent(
        llm,
        tools=[web_search],
    )

    question = HumanMessage("Who is the current mayor of Leon, Spain?")

    response = agent.invoke(
        {"messages": [question]},
    )

    print("--- Answering a question with the web search tool ---")
    rich.print(response["messages"][-1].content)
    print("-" * 80)


def main() -> None:
    """Main entry point for the application."""
    invoke_tool()
    print("=" * 80)

    agent_with_tool()
    print("=" * 80)

    agent_with_web_search_tool()
    print("=" * 80)


if __name__ == "__main__":
    main()
