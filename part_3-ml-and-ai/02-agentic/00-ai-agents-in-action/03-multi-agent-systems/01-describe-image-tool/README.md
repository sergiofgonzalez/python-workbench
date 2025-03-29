# Tool that describe an image

A tool that can be used in an agentic solution to describe an image.
There are two implementations:
+ Using the SDK
+ Using the API: despite following documentation, it fails with a 404.

To configure populate the .env file with:

```INI
OPENAI_TYPE = "azure" # "azure" for Azure OpenAI client or "openai" for the native OpenAI API client

# Azure OpenAI API configuration
AZURE_OPENAI_ENDPOINT =
AZURE_OPENAI_API_KEY =
AZURE_OPENAI_API_VERSION = 
```