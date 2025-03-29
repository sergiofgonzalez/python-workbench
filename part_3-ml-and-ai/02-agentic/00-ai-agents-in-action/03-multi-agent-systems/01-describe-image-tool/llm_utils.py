"""Utilities for interacting with Azure OpenAI's Language Learning Model (LLM)."""

import json
import os
from typing import NamedTuple

from dotenv import load_dotenv
from openai import AzureOpenAI, OpenAI

load_dotenv(override=True)


# Azure OpenAI configuration
class AzureOpenAIConfig(NamedTuple):
    """Configuration for Azure OpenAI."""

    subscription_key: str
    api_version: str
    azure_endpoint: str


class OpenAIConfig(NamedTuple):
    """Configuration for OpenAI."""

    api_key: str
    base_url: str | None
    default_headers: dict[str, str] | None
    default_query: dict[str, str] | None


openai_type = os.getenv("OPENAI_TYPE", "azure").lower()


def _load_azure_openai_config() -> AzureOpenAIConfig:
    """Load Azure OpenAI configuration from environment variables."""
    if not (api_version := os.getenv("AZURE_OPENAI_API_VERSION")):
        msg = "Please configure your Azure OpenAI API version"
        raise ValueError(msg)

    if not (endpoint := os.getenv("AZURE_OPENAI_ENDPOINT")):
        msg = "Please configure your Azure OpenAI endpoint"
        raise ValueError(msg)

    if not (subscription_key := os.getenv("AZURE_OPENAI_API_KEY")):
        msg = "Please configure your Azure OpenAI API key"
        raise ValueError(msg)

    return AzureOpenAIConfig(
        api_version=api_version,
        azure_endpoint=endpoint,
        subscription_key=subscription_key,
    )


def _load_openai_config() -> OpenAIConfig:
    """Load OpenAI configuration from environment variables."""
    if not (api_key := os.getenv("OPENAI_API_KEY")):
        msg = "Please configure your OpenAI API key"
        raise ValueError(msg)

    base_url = os.getenv("OPENAI_BASE_URL")
    default_headers = os.getenv("OPENAI_DEFAULT_HEADERS")
    default_query = os.getenv("OPENAI_DEFAULT_QUERY")

    return OpenAIConfig(
        api_key=api_key,
        base_url=base_url,
        default_headers=default_headers,
        default_query=default_query,
    )


def _get_client(**kwargs: dict) -> OpenAI | AzureOpenAI:
    """Get an OpenAI client."""
    if openai_type == "azure":
        azure_openai_config = _load_azure_openai_config()
        return AzureOpenAI(
            api_version=azure_openai_config.api_version,
            azure_endpoint=azure_openai_config.azure_endpoint,
            api_key=azure_openai_config.subscription_key,
        )
    if openai_type == "openai":
        openai_config = _load_openai_config()
        if "deployment" in kwargs:
            base_url = (
                f"{openai_config.base_url}/openai/deployments/{kwargs['deployment']}"
            )
        else:
            base_url = openai_config.base_url

        try:
            default_headers = json.loads(openai_config.default_headers)
        except json.JSONDecodeError as e:
            msg = "Invalid JSON for OpenAI default headers"
            raise ValueError(msg) from e

        try:
            default_query = json.loads(openai_config.default_query)
        except json.JSONDecodeError as e:
            msg = "Invalid JSON for OpenAI default query"
            raise ValueError(msg) from e

        return OpenAI(
            base_url=base_url,
            api_key=openai_config.api_key,
            default_headers=default_headers,
            default_query=default_query,
        )
    msg = f"Unknown OpenAI type: {openai_type}"
    raise ValueError(msg)


def prompt_llm(
    messages: list[str],
    model: str,
    **kwargs: dict[str],
) -> str:
    """Prompt an Azure OpenAI LLM using the Chat Completions SDK with the given data."""
    client = _get_client(**kwargs)

    if "deployment" in kwargs:
        model = kwargs["deployment"]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content
