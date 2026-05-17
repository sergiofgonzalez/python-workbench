"""Illustrates the basics of configuring a system prompt for your agent."""

import os

import rich
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

load_dotenv()


def agent_with_system_prompt() -> None:
    """Create a simple agent using LangChain."""
    llm = ChatOpenAI(
        model="bedrock-claude-sonnet-4-5",
        api_key=SecretStr(os.environ["LITELLM_API_KEY"]),
        base_url=os.getenv("LITELLM_BASE_URL"),
    )

    system_prompt = """
    You are a science fiction writer. Create a capital city at the user's request.
    """

    agent = create_agent(llm, system_prompt=system_prompt)

    response = agent.invoke(
        {"messages": [HumanMessage("What is the capital of the moon?")]},
    )

    rich.print("-" * 80)
    rich.print(response["messages"][-1].content)
    rich.print("=" * 80)


def agent_with_fine_tuned_system_prompt_v1() -> None:
    """Create an agent with a fine-tuned system prompt."""
    llm = ChatOpenAI(
        model="bedrock-claude-sonnet-4-5",
        api_key=SecretStr(os.environ["LITELLM_API_KEY"]),
        base_url=os.getenv("LITELLM_BASE_URL"),
    )

    system_prompt = """
    You are a science fiction write, create a capital city at the users request.

    User: What is the capital of Mars?
    Scifi Writer: Marsialis

    User: What is the capital of the Moon?
    Scifi Writer: Luna city
    """

    agent = create_agent(llm, system_prompt=system_prompt)

    response = agent.invoke(
        {"messages": [HumanMessage("What is the capital of the moon?")]},
    )

    rich.print("-" * 80)
    rich.print(response["messages"][-1].content)
    rich.print("=" * 80)


def agent_with_fine_tuned_system_prompt_v2() -> None:
    """Create an agent with a fine-tuned system prompt."""
    llm = ChatOpenAI(
        model="bedrock-claude-sonnet-4-5",
        api_key=SecretStr(os.environ["LITELLM_API_KEY"]),
        base_url=os.getenv("LITELLM_BASE_URL"),
    )

    system_prompt = """
    You are a science fiction write, create a capital city at the users request.

    Please keep to the below structure.

    Name: The name of the capital city

    Location: Where it is based

    Vibe: 2-3 words to describe its vible

    Economy: Main industries
    """

    agent = create_agent(llm, system_prompt=system_prompt)

    response = agent.invoke(
        {"messages": [HumanMessage("What is the capital of the moon?")]},
    )

    rich.print("-" * 80)
    rich.print(response["messages"][-1].content)
    rich.print("=" * 80)


def main() -> None:
    """Main entry point for the application."""
    agent_with_system_prompt()
    agent_with_fine_tuned_system_prompt_v1()
    agent_with_fine_tuned_system_prompt_v2()


if __name__ == "__main__":
    main()
