# Basics of prompt engineering: using clear instructions

## Program description

The program starts by loading all the JSONL files in the `prompts/` directory. Then, it displays the list of files as numeric choices and allows the user to choose an option. After the selection is done, the prompts are submitted to the LLM and the response is printed.

## Configuration and usage notes

To run the project you either need an OpenAI or Azure Open AI subscription.

The following pieces of information need to be provided (either using environment variables or a .env file):

```INI
OPENAI_TYPE = "openai" # "azure" for Azure OpenAI client or "openai" for the native OpenAI API client

# Azure OpenAI API configuration
AZURE_OPENAI_ENDPOINT = "<the Azure Open AI Endpoint as found in Azure Portal>"
AZURE_OPENAI_API_KEY = "<the Azure Open AI Key as found in Azure Portal>"
AZURE_OPENAI_API_VERSION = "<the Azure OpenAI version from https://learn.microsoft.com/en-us/azure/ai-services/openai/api-version-deprecation>"

# Azure OpenAI API configuration via native OpenAI client
OPENAI_API_KEY = ${AZURE_OPENAI_API_KEY}
OPENAI_BASE_URL = ${AZURE_OPENAI_ENDPOINT}
OPENAI_DEFAULT_HEADERS = "{\"api-key\": \"${AZURE_OPENAI_API_KEY}\"}"
OPENAI_DEFAULT_QUERY = "{\"api-version\": \"${AZURE_OPENAI_API_VERSION}\"}"
```

The project has been tested with the native Azure OpenAI client and the native client pointing to an Azure Open AI deployment.

In any case, when using a model hosted on Azure OpenAI, you need to use the `deployment` as found in the Azure AI Foundry &raquo; Deployments section:

```python
# use GPT4 on Azure OpenAI
response = prompt_llm(
    messages,
    model="gpt4",
    deployment="chatgpt4-turbo",  # only required for Azure OpenAI
)

# Use o3-mini on Azure OpenAI
response = prompt_llm(
    messages,
    model="o3-mini",
    deployment="o3-mini",  # only required for Azure OpenAI
)
```