"""Illustrates how to use Pydantic to give structure to the agent's response."""

import os

import rich
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, SecretStr

load_dotenv()


class CapitalInfo(BaseModel):
    """Model for the capital information."""

    name: str
    location: str
    vibe: str
    economy: str


def main() -> None:
    """Main entry point for the application."""
    llm = ChatOpenAI(
        model="bedrock-claude-sonnet-4-5",
        api_key=SecretStr(os.environ["LITELLM_API_KEY"]),
        base_url=os.getenv("LITELLM_BASE_URL"),
    )

    system_prompt = """
    You are a science fiction writer. Create a capital city at the user's request.
    """

    agent = create_agent(
        llm,
        system_prompt=system_prompt,
        response_format=CapitalInfo,
    )

    question = HumanMessage("What is the capital of the moon?")

    response = agent.invoke(
        {"messages": [question]},
    )

    rich.print("-" * 80)
    rich.print(response["structured_response"])
    rich.print("=" * 80)

    moon_capital = response["structured_response"]

    print(
        f"The capital of the moon is {moon_capital.name} "
        f"and it is {moon_capital.location}.",
    )


if __name__ == "__main__":
    main()
