"""Embedding function using OpenAI embedding model"""
import os
from openai import AzureOpenAI

az_open_ai_client = AzureOpenAI(
    api_key="<the-api-key-here>", #os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-05-15", #"2023-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

def embed(texts):
    """Embed a list of texts using OpenAI embedding model"""
    response = az_open_ai_client.embeddings.create(
        input=texts,
        model="csdep-text-embedding-ada-002" # "text-embedding"  # Actually, this is the deployment name (model name is text_embedding-3-small)
    )
    return list(map(lambda n: n.embedding, response.data))