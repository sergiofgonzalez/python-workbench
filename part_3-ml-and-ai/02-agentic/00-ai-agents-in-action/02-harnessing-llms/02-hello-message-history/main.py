"""Application main program."""

import os
from pprint import pprint

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()


model_name = "o3-mini"
deployment = "o3-mini"
api_version = "2024-12-01-preview"

if not (subscription_key := os.getenv("AZURE_OPENAI_API_KEY")):
    msg = "Please configure your Azure OpenAI API key"
    raise ValueError(msg)

if not (endpoint := os.getenv("AZURE_OPENAI_ENDPOINT")):
    msg = "Please configure your Azure OpenAI endpoint"
    raise ValueError(msg)


client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)


def ask_gpt(messages: list[str]) -> str:
    """Send user message to a chat completions LLM and relay the response."""
    return client.chat.completions.create(
        model=model_name,
        messages=messages,
    )


def main() -> None:
    """Application entry point."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Where is Luengos de los Oteros?"},
        {
            "role": "assistant",
            "content": "Luengos de los Oteros is a small town of the municipality of León, Spain.",
        },
        {
            "role": "user",
            "content": "Can you tell me an interesting fact about that place?",
        },
    ]
    response = ask_gpt(messages)
    pprint(response)

if __name__ == "__main__":
    main()
