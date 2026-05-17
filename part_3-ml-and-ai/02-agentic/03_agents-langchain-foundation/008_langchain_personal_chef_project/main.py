"""Illustrates the techniques in this section to build a personal chef agent."""

import base64
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_core.runnables import ensure_config
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import SecretStr
from rich.console import Console
from tavily import TavilyClient

load_dotenv()

llm = ChatOpenAI(
    model="bedrock-claude-sonnet-4-5",
    api_key=SecretStr(os.environ["LITELLM_API_KEY"]),
    base_url=os.getenv("LITELLM_BASE_URL"),
)

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> dict[str, Any]:
    """Search the web for information on the given query."""
    return tavily_client.search(query)


def personal_chef_agent_text_only() -> None:
    """Create a Personal Chef agent using text only."""

    def agentic_loop() -> None:
        """The main loop of the agent executed until user is satisfied."""
        question = HumanMessage(
            [
                {"type": "text", "text": user_input},
            ],
        )

        response = agent.invoke(
            {"messages": [question]},
            config,
        )

        console.print(response["messages"][-1].content, style="green")
        console.print("-" * 80, style="green")

    system_prompt = """
        You are a chef in charge of helping users identify basic dishes to prepare
        at home with leftovers. You will be given a list of ingredients and you
        will search the web for recipes and choose a simple recipe that can be made
        with those ingredients.
        """

    agent = create_agent(
        llm,
        system_prompt=system_prompt,
        checkpointer=InMemorySaver(),
        tools=[web_search],
    )

    config = ensure_config({"configurable": {"thread_id": "1"}})

    console = Console()
    console.print(
        "[green]🤖 Hi! I am your personal chef assistant.\nI can help you find "
        "recipes based on the ingredients you have at home.[/green]",
    )
    user_input = console.input("[green]🤖 What ingredients do you have? [/green]")
    console.print(f"You: {user_input}", style="cyan")
    while True:
        agentic_loop()
        user_input = console.input(
            "[green]🤖 Do you have any doubts about the recipe? (yes/no) [/green]",
        )
        if user_input.lower() == "no":
            break
        user_input = console.input(
            "[green]🤖 What else you'd like to ask? [/green]",
        )


def get_image_type_from_path(img_path: Path) -> str:
    """Get the image type from the file extension."""
    ext = img_path.suffix.lstrip(".").lower()
    match ext:
        case "jpg" | "jpeg":
            return "jpeg"
        case "png":
            return "png"
        case "gif":
            return "gif"
        case _:
            msg = f"Unsupported image type: {ext}"
            raise ValueError(msg)


def personal_chef_agent_with_images() -> None:
    """Create a Personal Chef agent using text and images."""

    def agentic_loop() -> None:
        """The main loop of the agent executed until user is satisfied."""
        if user_input.startswith("img:"):
            img_path = Path(user_input[len("img:") :].strip())
            img_type = get_image_type_from_path(img_path)
            with img_path.open("rb") as f:
                img_bytes = f.read()

            img_b64 = base64.b64encode(img_bytes).decode("utf-8")

            question = HumanMessage(
                [
                    {"type": "text", "text": "Identify the ingredients in the image."},
                    {
                        "type": "image",
                        "base64": img_b64,
                        "mime_type": f"image/{img_type}",
                    },
                ],
            )
        else:
            question = HumanMessage(
                [
                    {"type": "text", "text": user_input},
                ],
            )

        response = agent.invoke(
            {"messages": [question]},
            config,
        )

        console.print("🤖", response["messages"][-1].content, style="green")
        console.print("-" * 80, style="green")

    system_prompt = """
        You are a chef in charge of helping users identify basic dishes to prepare
        at home with leftovers. You will be given a list of ingredients (via text
        and/or images) and you will search the web for recipes and choose a simple
        recipe that can be made with those ingredients.

        When given an image, start the recipe by identifying the ingredients you
        identified in the image. Do not wait for the user to confirm, simply give
        the recipe based on the ingredients you identified in the image.
        """

    agent = create_agent(
        llm,
        system_prompt=system_prompt,
        checkpointer=InMemorySaver(),
        tools=[web_search],
    )

    config = ensure_config({"configurable": {"thread_id": "1"}})

    console = Console()
    console.print(
        "[green]🤖 Hi! I am your personal chef assistant.\nI can help you find "
        "recipes based on the ingredients you have at home.\n"
        "You can also provide images of your ingredients.[/green]",
    )
    console.print(
        "[green]🤖 What ingredients do you have?\n"
        "(To provide an image, please type img: <path_to_image>)[/green]",
    )
    user_input = console.input("😎: ")
    while True:
        agentic_loop()
        console.print(
            "[green]🤖 Do you have any doubts about the recipe? (yes/no) [/green]",
        )
        user_input = console.input(
            "😎: ",
        )
        if user_input.lower() == "no":
            break
        console.print("[green]🤖 What else you'd like to ask?[/green]")
        user_input = console.input(
            "😎: ",
        )


def main() -> None:
    """Main entry point for the application."""
    personal_chef_agent_text_only()
    print("=" * 80)

    personal_chef_agent_with_images()
    print("=" * 80)


if __name__ == "__main__":
    main()
