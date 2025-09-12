"""Simple chat application using Azure AI Foundry SDK."""

import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

project_endpoint = os.getenv("PROJECT_ENDPOINT")
deployment_name = os.getenv("DEPLOYMENT_NAME")


def main() -> None:
    """Application entry point."""
    if not project_endpoint:
        msg = "PROJECT_ENDPOINT environment variable is not set."
        raise ValueError(msg)
    if not deployment_name:
        msg = "DEPLOYMENT_NAME environment variable is not set."
        raise ValueError(msg)

    try:
        # Get project client
        print("Instantiate the project client...")
        project_client = AIProjectClient(
            credential=DefaultAzureCredential(),
            endpoint=project_endpoint,
        )

        # Get chat client from the project's client
        chat_client = project_client.inference.get_azure_openai_client(
            api_version="2025-04-01-preview",
        )

        # Get a chat completion
        user_prompt = input("Enter your question: ")
        response = chat_client.responses.create(
            model=deployment_name,
            input=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_prompt},
            ],
        )

        # Print the response
        print(f"Assistant: {response.output_text}")
    except Exception as ex:  # noqa: BLE001
        print(f"Oops: {ex}")


if __name__ == "__main__":
    main()
