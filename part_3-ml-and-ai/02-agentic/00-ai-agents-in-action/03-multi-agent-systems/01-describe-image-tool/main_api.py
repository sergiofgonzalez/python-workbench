"""Script using Azure OpenAI API (not the SDK) to describe the contents of an image."""

import base64
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(override=True)


def encode_image(image_path: Path) -> str:
    """Encode an image as a base64 string."""
    with image_path.open("rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def describe_image(image_path: Path, model: str, deployment_name: str | None) -> str:
    """Describe the contents of an image with an LLM."""
    if not (api_key := os.getenv("AZURE_OPENAI_API_KEY")):
        msg = "Azure OpenAI API Key not found"
        raise ValueError(msg)
    if not (endpoint := os.getenv("AZURE_OPENAI_ENDPOINT")):
        msg = "Azure OpenAI Endpoint not found"
        raise ValueError(msg)
    if not (api_version := os.getenv("AZURE_OPENAI_API_VERSION")):
        msg = "Azure OpenAI API Version not found"
        raise ValueError(msg)
    if not model:
        msg = "Model must be specified"
        raise ValueError(msg)
    if not deployment_name:
        print("Warning: Deployment name not specified, using model name")
        deployment_name = model

    base64_image_str = encode_image(image_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "api-key": api_key,
    }
    json_payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What is in this image?",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image_str}",
                        },
                    },
                ],
            },
        ],
        "max_tokens": 300,
    }

    url = f"{endpoint}openai/deployments/{deployment_name}/completions?api_version={api_version}"  # noqa: E501
    response = requests.post(
        url,
        headers=headers,
        json=json_payload,
        timeout=30,
    )
    if response.status_code != 200:  # noqa: PLR2004
        msg = f"Failed to describe image: {response.status_code}"
        raise ValueError(msg)

    return response.json()["choices"][0]["message"]


def main() -> None:
    """Application entry point."""
    image_path = Path("images", "scopes.png")
    model = "o1"
    deployment_name = "o1"

    try:
        description = describe_image(image_path, model, deployment_name)
        print(description)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
