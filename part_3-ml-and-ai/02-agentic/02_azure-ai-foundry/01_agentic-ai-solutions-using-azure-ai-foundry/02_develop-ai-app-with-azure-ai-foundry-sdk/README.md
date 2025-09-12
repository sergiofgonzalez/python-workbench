# Milestone 1 &raquo; Module 2
[Develop and AI app with Azure AI Foundry SDK](https://learn.microsoft.com/en-us/training/modules/ai-foundry-sdk/)

Learning objectives:

Learning objectives:

+ Describe capabilities of the Azure AI Foundry SDK.
+ Use the Azure AI Foundry SDK to work with connections in projects.
+ Use the Azure AI Foundry SDK to develop an AI chat app.

## Intro

The Azure AI Foundry SDK brings together access to common services and a set of code libraries making it easier for developers to write the code needed to build effective AI apps on Azure.

## What is the Azure AI Foundry SDK

Azure AI Foundry SDK enables developers to connect to a project, access the resource connections and models in that project, and use them to perform AI operations (such as sending prompts to a generative AI model and processing the responses).

Multiple language specific SDKs are available, including:
+ Python
+ .Net
+ JavaScript

Azure AI Foundry SDK is published in PyPI under the name `azure-ai-projects`.

### Using the SDK to connect to a project

Each Azure AI Foundry project has a unique endpoint, which can be found in the the "Overview" section of the [AI Foundry Portal](https://ai.azure.com).

In that section, you will find a "Libraries" section. Choose Azure AI Foundry to find the Azure AI Foundry project endpoint.

Note that under "Libraries" you will also be able to get:

+ An endpoint for Azure OpenAI Service APIs in the project's resource.
+ An endpoint for the Azure AI Services (such as Azure AI Vision) in the project's resource.

The function `AIProjectClient()` provides a programmatic proxy for the project:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project_endpoint = "https://<the-project-endpoint>"
project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=project_endpoint
)
```

| NOTE: |
| :---- |
| To enable the authentication shown above, you need to install the `azure-identity` package in addition to the `azure-ai-projects` package. |

To access the project, the code must be run in the context of an authenticated Azure session. For example, it will be sufficient to do `az-login`.

| EXAMPLE: |
| :------- |
| See [01: Connect to a project](01_connect-to-prj/) for a runnable example. |

## Work with project connections

Each Azure AI Foundry project includes connected resources, which are defined both at the resource and project level.

Each resource is a connection to an external service, such as Azure Storage, Azure AI Search, Azure OpenAI, ...

You can use the SDK to connect to a project and retrieve the connections that ultimately will allow you to consume the services.

These connections can be accessed through the `connections` object on the `project_client`.

The object exposes:

+ `connections.list()`: returns a collection of connection objects, each representing a connection in the project. You can use the optional parameter `connection_type` with a valid enumeration such as `ConnectionType.AZURE_OPEN_AI` to filter the results by type.

+ `connections.get(connection_name, include_credentials)`: Returns a connection object for the connection with the name specified. If the `include_credentials` is `True` (the default value is False), the credentials required to connect to the given connection are also returned. That way you can connect right away to the associated resource.

| EXAMPLE: |
| :------- |
| See [02: list connections](02_list-connections/) for a runnable example in which not only connections are listed, but also, the result from `connections.get()` is used to work with a connected resource. |

## Create a chat client

When your model is deployed on an Azure AI Foundry project, you can use Azure AI Foundry SDK to retrieve a project client, from which you can then get an authenticated OpenAI chat client for any models deployed in the project's Azure AI Foundry resource.

This approach makes it easy to write code that consumes models deployed in your project, and allows you to switch between them easily by changing the model's *deployment name* paramenter. Additionally, this approach will work for both OpenAI and non-OpenAI models.

| NOTE: |
| :---- |
| You can use Azure OpenAI SDK to connect directly to an OpenAI model. |


The following snippet illustrates how you can get an OpenAI client with which to chat with a model that has been deployed in the project's Azure AI Foundry resource.

| NOTE: |
| :---- |
| You will need to install `openai` package. |


```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


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
    except Exception as ex:
        print(ex)
```

| EXAMPLE: |
| :------- |
| See [03: chat client](03_chat-client/) and [04: chat client (using OpenAI Responses API)](04_chat-client-responses-api/) for a couple of runnable examples that interact with deployed models using Azure AI Foundry SDK. |

## Exercise: Create a GenAI chat app

See [05: Chat app](05_chat-app/) for a very basic chat application that includes some memory so that you can ask follow up questions to a one given.