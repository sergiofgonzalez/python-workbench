"""
Script using Azure OpenAI SDK to describe the contents of an image, as the API won't work.
"""

import base64
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from llm_utils import prompt_llm


def encode_image(image_path: Path) -> str:
    """Encode an image as a base64 string."""
    with image_path.open("rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def describe_image(image_path: Path, model: str, deployment_name: str | None) -> str:
    """Describe the contents of an image with an LLM."""
    base64_image_str = encode_image(image_path)
    messages = [
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
    ]
    return prompt_llm(
        messages=messages,
        model=model,
        deployment=deployment_name,
        max_tokens=300,
    )


def main() -> None:
    """Application entry point."""
    image_path = Path("images", "scopes.png")
    model = "o1"
    deployment_name = "o1"
    description = describe_image(image_path, model, deployment_name)
    print(description)


if __name__ == "__main__":
    main()
