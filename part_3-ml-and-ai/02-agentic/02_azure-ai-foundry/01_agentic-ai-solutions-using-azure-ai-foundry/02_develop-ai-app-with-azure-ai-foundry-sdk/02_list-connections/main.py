"""List the connections of an Azure AI Foundry project.

Illustrates how to list the connections of an Azure AI Foundry project using
Azure AI Foundry SDK.
"""

import os
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

project_endpoint = os.getenv("PROJECT_ENDPOINT")
connection_name = os.getenv("STG_ACCOUNT_NAME")
container_name = os.getenv("CONTAINER_NAME")


def main() -> None:
    """Application entry point."""
    if not project_endpoint:
        msg = "PROJECT_ENDPOINT environment variable is not set."
        raise ValueError(msg)
    if not connection_name:
        msg = "STG_ACCOUNT_NAME environment variable is not set."
        raise ValueError(msg)
    if not container_name:
        msg = "CONTAINER_NAME environment variable is not set."
        raise ValueError(msg)

    # Get project client
    print("Instantiate the project client...")
    project_client = AIProjectClient(
        credential=DefaultAzureCredential(),
        endpoint=project_endpoint,
    )

    # List all the connections in the project
    print("List all the connections in the project...")
    connections = project_client.connections
    for connection in connections.list():
        print(f"{connection.name} ({connection.type})")

    # By default include_credentials is set to False
    connection = connections.get(connection_name, include_credentials=True)
    print(f"\nConnection details for {connection_name}:")
    print(f"Name: {connection.name}")
    print(f"Type: {connection.type}")

    # Accessing the storage account to pull a file
    # Download 'architecture.png' from 'files' container
    print("\nDownloading 'architecture.png' from 'files' container...")

    blob_service_client = BlobServiceClient(
        account_url=connection["target"],
        credential=connection.credentials["key"],
    )
    container_client = blob_service_client.get_container_client(container_name)
    Path(container_name).mkdir(exist_ok=True)
    print(f"Downloading all blobs in '{container_name}' container...")
    for blob in container_client.list_blobs():
        print(f"Downloading {blob.name}...")
        blob_client = container_client.get_blob_client(blob.name)
        download_path = Path(container_name, blob.name)
        with download_path.open("wb") as file:
            file.write(blob_client.download_blob().readall())
        print(f"Downloaded '{blob.name}' to {download_path}")


if __name__ == "__main__":
    main()
