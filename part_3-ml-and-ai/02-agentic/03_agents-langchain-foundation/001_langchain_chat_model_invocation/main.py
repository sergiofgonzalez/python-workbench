"""Illustrates the basics of invoking a chat model using LangChain.."""

import os

import rich
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()


def invoke_model_bare() -> None:
    """Illustrates the bare minimum of invoking a chat model using LangChain."""
    model = init_chat_model(
        model="gpt-5-mini",
        api_key=os.environ["LITELLM_API_KEY"],
        base_url=os.environ["LITELLM_BASE_URL"],
        # model parameters
        temperature=1.0,
    )
    response = model.invoke("What is the capital of the Moon?")
    rich.print("-" * 80)
    rich.print(response)
    rich.print("=" * 80)
    rich.print("-" * 80)
    rich.print(f"{response.content=}")
    rich.print("=" * 80)
    rich.print("-" * 80)
    rich.print(response.response_metadata)
    rich.print("=" * 80)


def invoke_model_with_temperature() -> None:
    """Illustrates invoking a chat model with a specific temperature."""
    model = init_chat_model(
        model="gpt-5-mini",
        api_key=os.environ["LITELLM_API_KEY"],
        base_url=os.environ["LITELLM_BASE_URL"],
        # model parameters
        temperature=1.0,
    )
    response = model.invoke("What is the capital of the Moon?")
    rich.print("-" * 80)
    rich.print(response)
    rich.print("=" * 80)
    rich.print("-" * 80)
    rich.print(f"{response.content=}")
    rich.print("=" * 80)
    rich.print("-" * 80)
    rich.print(response.response_metadata)
    rich.print("=" * 80)


def main() -> None:
    """Main entry point for the application."""
    invoke_model_bare()
    input("Press Enter to continue...")
    invoke_model_with_temperature()
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
