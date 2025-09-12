"""Connect to Azure AI Foundry project.

Illustrates how to connect to an Azure AI Foundry project using Azure AI Foundry SDK.
"""

import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

project_endpoint = os.getenv("PROJECT_ENDPOINT")


def main() -> None:
    """Application entry point."""
    if not project_endpoint:
        msg = "PROJECT_ENDPOINT environment variable is not set."
        raise ValueError(msg)

    project_client = AIProjectClient(  # noqa: F841
        credential=DefaultAzureCredential(),
        endpoint=project_endpoint,
    )
    print("Client successfully instantiated.")


if __name__ == "__main__":
    main()
