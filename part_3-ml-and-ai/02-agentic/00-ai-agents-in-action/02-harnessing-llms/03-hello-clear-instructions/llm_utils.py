import os

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


def prompt_llm(
    messages: list[str],
    model: str = model_name,
    deployment: str = deployment,
    api_version: str = api_version,
    api_key: str = subscription_key,
) -> str:
    """Prompt an Azure OpenAI LLM using the Chat Completions SDK with the given data."""
    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content
