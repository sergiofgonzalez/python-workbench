"""Illustrates how to enable short-term memory in LangChain agents."""

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.runnables import ensure_config
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import SecretStr

load_dotenv()

llm = ChatOpenAI(
    model="bedrock-claude-sonnet-4-5",
    api_key=SecretStr(os.environ["LITELLM_API_KEY"]),
    base_url=os.getenv("LITELLM_BASE_URL"),
)


def agent_with_no_memory() -> None:
    """Create a simple agent using LangChain."""
    agent = create_agent(llm)

    question = HumanMessage("Hi, I'm Sergio and my favorite color is blue.")

    response = agent.invoke(
        {"messages": [question]},
    )

    print(response["messages"][-1].content)
    print("-" * 80)

    question = HumanMessage("Who am I and what's my favorite color?")

    response = agent.invoke(
        {"messages": [question]},
    )

    print(response["messages"][-1].content)
    print("-" * 80)


def agent_with_memory() -> None:
    """Create a simple agent using LangChain with memory."""
    agent = create_agent(
        llm,
        checkpointer=InMemorySaver(),
    )

    config = ensure_config({"configurable": {"thread_id": "1"}})

    question = HumanMessage("Hi, I'm Sergio and my favorite color is blue.")

    response = agent.invoke(
        {"messages": [question]},
        config,
    )

    print(response["messages"][-1].content)
    print("-" * 80)

    question = HumanMessage("Who am I and what's my favorite color?")

    response = agent.invoke(
        {"messages": [question]},
        config,
    )

    print(response["messages"][-1].content)
    print("-" * 80)


def main() -> None:
    """Application entry point."""
    print("=== Agent with no memory ===")
    agent_with_no_memory()
    print("=" * 80)

    print("=== Agent with memory ===")
    agent_with_memory()
    print("=" * 80)


if __name__ == "__main__":
    main()
