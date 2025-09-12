# Milestone 1 &raquo; Module 1
> [Plan and prepare to develop AI solutions on Azure](https://learn.microsoft.com/en-us/training/modules/prepare-azure-ai-development/?source=docs)

Learning objectives:

+ Identify common AI capabilities that you can implement in applications.
+ Describe Azure AI Services and considerations for using them.
+ Describe Azure AI Foundry and considerations for using it.
+ Identify appropriate developer tools and SDKs for an AI project.
+ Describe considerations for responsible AI.

## Intro

The growth in the use of AI and Gen AI means that developers are increasingly required to create comprehensive AI solutions. These solutions need to combine ML models, AI services, prompt engineering solutions, and custom code.

Azure provides multiple services to create AI solutions. However, before embarking on an AI development project, it's useful to consider available options for services, tools, and frameworks as well as some principles and practices that can help you succeed.

Azure AI Foundry is a comprehensive platform for AI development on Azure.

## What is AI?

The term AI covers a wide range of software capabilities that enable apps to exhibit human-like behavior.

In today's technological landscape, AI solutions are built on ML models that encapsulate semantic relationships found in huge quantities of data; enabling apps to appear to interpret input in various formats, reason over the input data, and generate appropriate responses and predictions.

Common AI capabilities include:

| Capability | Description |
| :--------- | :---------- |
| Generative AI (Gen AI) | The ability to generate original responses to natural language prompts. |
| Agents | Gen AI appliations that can respond to user input or assess situations autonomously, and take appropriate actions. |
| Computer Vision | The ability to accept, interpret, and process visual input from images, videos, and live camera streams. |
| Speech | The ability to recognize and synthesize speech. |
| Natural Language Processing | The ability to process natural language in written or spoken form, analyze it, identify key points, and generate summaries or categorizations. |
| Information Extraction | The ability to use computer vision, speech, and natural language processing to extract key information from documents, forms, images, recordings, and other kind of content. |
| Decision support | The ability to use historic data and learned correlations to make predictions that support business decision making. |

Identifying the specific AI capabilities you want to include in your app can help identify the most appropriate AI services that you'll need to provision, configure, and use in your solution.

## A closer look at Gen AI

Gen AI uses language models to respond to natural language prompts, enabling you to build conversational apps and agents that support research, content creation, and task automation in ways that were previously unimaginable.

The language models used in Gen AI can be LLMs that have been trained on huge volumes of data and include many millions of parameters; or they can be Small Language Models (SLM) that are optimized for specific scenarios with lower overhead.

Language models commonly respond to text-based prompts with natural language text, though increasingly new multi-model models are able to handle image or speech prompts and respond by generating text, code, speech, or images.

## Azure AI Services

Azure AI services is a set of OOB prebuilt APIs and models that you can integrate into your apps.

The following table lists some commonly used Azure AI services.

| Service | Icon | Description |
| :------ | :--- | :---------- |
| Azure OpenAI | ![Azure OpenAI](https://learn.microsoft.com/en-us/training/wwl-data-ai/prepare-azure-ai-development/media/open-ai.png) | Azure OpenAI in Foundry Models provides access to OpenAI generative AI models including the GPT family of large and small language models and DALL-E image generation models with a scalable and securable cloud services on Azure |
| Azure AI Vision | ![Azure AI Vision](https://learn.microsoft.com/en-us/training/wwl-data-ai/prepare-azure-ai-development/media/vision.png) | The Azure AI Vision service provides a set of models and APIs that you can use to implement common computer vision functionality in an application. With the AI Vision service, you can detect common objects in images, generate captions, descriptions, and tags based on image contents, and read text in images. |
| Azure AI Speech | ![Azure AI Speech](https://learn.microsoft.com/en-us/training/wwl-data-ai/prepare-azure-ai-development/media/speech-service.png) | The Azure AI Speech service provides APIs that you can use to implement text-to-speech transformation, as well as specialized speech-based capabilities like speaker recognition and translation. |
| Azure AI Language | ![Azure AI Language](https://learn.microsoft.com/en-us/training/wwl-data-ai/prepare-azure-ai-development/media/language.png) | The Azure AI Language service provides models and APIs that you can use to analyze natural language text and perform tasks such as entity extraction, sentiment analysis, and summarization. The AI Language service also provides functionality to help you build conversational language model and question answering solutions. |
| Azure AI Foundry Content Safety | ![Azure AI Foundry Content Safety](https://learn.microsoft.com/en-us/training/wwl-data-ai/prepare-azure-ai-development/media/content-safety.png) | Azure AI Foundry Content Safety provides developers with access to advanced algorithms for processing images and text and flagging content that is potentially offensive, risky, or otherwise undesirable. |
| Azure AI Translator | ![Azure AI Translator](https://learn.microsoft.com/en-us/training/wwl-data-ai/prepare-azure-ai-development/media/translator.png) | The Azure AI Translator service uses state-of-the-art language models to translate text between a large number of languages. |
| Azure AI Face | ![Azure AI Face](https://learn.microsoft.com/en-us/training/wwl-data-ai/prepare-azure-ai-development/media/face.png) | The Azure AI Face service is a specialist computer vision implementation that can detect, analyze, and recognize human faces. Because of the potential risks associated with personal identification and misuse of this capability, access to some feature of the AI Face service are restricted to approved customers. |
| Azure AI Custom Vision | ![Azure AI Custom Vision](https://learn.microsoft.com/en-us/training/wwl-data-ai/prepare-azure-ai-development/media/custom-vision.png) | The Azure AI Custom Vision service enables you to train and use custom computer vision models for image classification and object detection. |
| Azure AI Document Intelligence | ![Azure AI Document Intelligence](https://learn.microsoft.com/en-us/training/wwl-data-ai/prepare-azure-ai-development/media/document-intelligence.png) | With Azure AI Document Intelligence, you can use pre-built or custom models to extract fields from complex documents such as invoices, receipts, and forms. |
| Azure AI Content Understanding | ![Azure AI Content Understanding](https://learn.microsoft.com/en-us/training/wwl-data-ai/prepare-azure-ai-development/media/content-understanding.png) | The Azure AI Content Understanding service provides multi-model content analysis capabilities that enable you to build models to extract data from forms and documents, images, videos, and audio streams. |
| Azure AI Search | ![Azure AI Search](https://learn.microsoft.com/en-us/training/wwl-data-ai/prepare-azure-ai-development/media/search.png) | The Azure AI Search service uses a pipeline of AI skills based on other Azure AI services and custom code to extract information from content and create a searchable index. AI Search is commonly used to create vector indexes for data that can then be used to ground prompts submitted to generative AI language models, such as those provided in Azure OpenAI. |

### Considerations for Azure AI services resources

The way to consume the services in the table above is:
+ You create one or more Azure AI resources in an Azure subscription.
+ Implement code in client applications to consume them.

In some cases, AI services include web-based visual interfaces that you can use to configure and test your resources.

#### Single service or multi-service resource?

Most Azure AI services can be provisioned as standalone resources, enabling you to create only the Azure resources you specifically need. Standalone services often include a free-tier SKU with limited functionality to enable you to test the service capabilities.

Each standalone Azure AI resource provides an endpoint and authorization keys that you can use to access the service securely from a client app.

Alternatively, you can provision a multi-service resource that encapsulates multiple AI services in a single Azure resource. This can simplify the management of applications that use multiple AI Capabilities.

There are two multi-service resources types:

| Resource | Icon | Description |
| :------- | :--- | :---------- |
| Azure AI services | ![Azure AI services](https://learn.microsoft.com/en-us/training/wwl-data-ai/prepare-azure-ai-development/media/cognitive-services.png) | The Azure AI Services resource type includes the following services, making them available from a single endpoint: <ul><li>Azure AI Speech</li><li>Azure AI Language</li><li>Azure AI Translator</li><li>Azure AI Vision</li><li>Azure AI Face</li><li>Azure AI Custom Vision</li><li>Azure AI Document Intelligence</li></ul> |
| Azure AI Foundry | ![Azure AI Foundry](https://learn.microsoft.com/en-us/training/wwl-data-ai/prepare-azure-ai-development/media/ai-services.png) | The Azure AI Foundry resource type includes the following services, and supports working with them through an Azure AI Foundry project: <ul><li>Azure OpenAI</li><li>Azure AI Speech</li><li>Azure AI Language</li><li>Azure AI Foundry Content Safety</li><li>Azure AI Translator</li><li>Azure AI Vision</li><li>Azure AI Face</li><li>Azure AI Document Intelligence</li><li>Azure AI Content Understanding</li></ul> |

#### Regional availability

Some services and models are available in only a subset of Azure regions.

See:
+ [Product availability table](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/table)
+ [Model Availability table](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability)

#### Cost

Azure AI services are charged based on usage, with different pricing schemes available depending on the specific services being used.

See:
+ [Azure AI services pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/)
+ [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator)

## Azure AI Foundry

Azure AI Foundry is a platform for AI development on Azure. While you can provision individual Azure AI services resources and build apps that consume them without it, the project organization, resource management, and AI development capabilities of Azure AI Foundry makes it the recommended way to build apps.

Azure AI Foundry provides the Azure AI Foundry portal, a web-based interface for working with AI projects. It also provides the Azure AI Foundry SDK, which you can use to build AI solutions programmatically.

### Foundry projects

Foundry projects are associated with an Azure AI Foundry resource in an Azure subscription. Foundry projects provide support for Azure AI Foundry models (including OpenAI models), Azure AI Foundry Agent Service, Azure AI services, and tools for evaluation and responsible AI development.

An Azure AI Foundry resource supports the most common AI development tasks to develop generative AI chat apps and agents. In most cases, using a Foundry project provides the right level of resource centralization and capabilities with a minimal amount of administrative resource management.

### Hub-based projects

Hub-based projects are associated with an Azure AI hub resource in an Azure subscription. Hub-based projects include and Azure AI Foundry resource, as well as managed compute, support form Prompt Flow development, and connected Azure storage and Azure key vault resources for secure data storage.

| NOTE: |
| :---- |
| Microsoft recommends sticking to Foundry projects. |

## Developer tools and SDKs

### Development tools and environments

Visual Studio Code is suitable for developing AI applications on Azure.

### The Azure AI Foundry for Visual Studio Code extension

When developing Azure AI Foundry based gen AI apps in VS Code, you can use the Azure AI Foundry for Visual Studio Code extension to simplify key tasks in the workflow including:
+ Creating a project
+ Selecting and deploying a model
+ Testing a model in the playground
+ Creating an agent

### Programming languages, APIs, and SDKs

You can develop AI applications using many common programming languages and frameworks, including C#, Python, Node, TypeScript, Java, and others.

Some common SDKs you should plan to install and use include:

+ The [Azure AI Foundry SDK](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/sdk-overview?pivots=programming-language-python), which enables you to write code to connect Azure AI Foundry projects and access resource connections, which you can then work with using service-specific SDKs.

+ The [Azure AI Foundry Models API](https://learn.microsoft.com/en-us/rest/api/aifoundry/modelinference/), which provides an interface for working with gen AI model endpoints hosted in Azure AI Foundry.

+ The [Azure OpenAI in Azure AI Foundry Models API](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference), which enables you to build chat apps based on OpenAI models hosted in Azure AI Foundry.

+ [Azure AI Services SDKs](https://learn.microsoft.com/en-us/azure/ai-services/reference/sdk-package-resources) &mdash; AI service-specific libraries for multiple programming languages and frameworks that enable you to consume Azure AI Services resources in your subscription. You can also use Azure AI Services directly through their [REST APIs](https://learn.microsoft.com/en-us/azure/ai-services/reference/rest-api-resources).

+ The [Azure AI Foundry Agent Service](https://learn.microsoft.com/en-us/azure/ai-services/agents/overview) which is accessed through the Azure AI Foundry SDK and can be integrated with frameworks like [Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/overview) to build comprehensive AI agent solutions.

## Responsible AI

It's important for sw engineers to consider the impact of their software on users and society in general, including considerations for its responsible use.

When the application is using AI, these considerations are particularly important due to the nature of how AI systems work and inform decisions; often based on probabilistic models, which are in turn dependent on the data with which they were trained.

The potential for harm to individuals or groups through incorrect predictions or misuse of AI capabilities is a major concern, and software engineers building AI-enabled solutions should apply due consideration to mitigate risks and ensure fairness, reliability, and adequate protection from harm or discrimination.

### Core Principles

The following section discuss some core principles for Responsible AI that have been adopted at Microsoft:

#### Fairness

All systems should treat all people fairly. For example, a loan approval application should make predictions without incorporating any bias based on gender, ethnicity, or other factors that might result in an unfair advantage or disadvantage to specific group of applicants.

Fairness of ML systems is a a highly active area of ongoing research, and some software solutions exist for evaluating, quantifying, and mitigating unfairness in ML models.

Fairness should be considered from the beginning of the app development process, carefully reviewing training data to ensure it's representative of all potentially affected subjects, and evaluating predictive performance for subsections of your user population throughout the development lifecycle.

#### Reliability and safety

AI-based software must be subjected to rigorous testing and deployment management to ensure that they work realiably and safely before release. Additionally, sw engineers must take into account the probabilistic nature of ML models, and apply appropriate thresholds when evaluating confidence scores for predictions.

#### Privacy and security

The ML models on which AI systems are based rely on large volumes of data, which may contain personal details that must be kept private. Even after models are trained and the system is in production, they use new data to make predictions or take action that may be subject to privacy or security concerns, so appropriate safeguards to protect data and customer content must be implemented.

#### Inclusiveness

AI systems should empower everyone and engage people. As a software engineer, you must optimize for inclusiveness to ensure that the design, development, and testing of your application includes input from as diverse a group of people as possible.

#### Transparency

AI systems should be understandable. Users should be made fully aware of the purpose of the system, how it works, and what limitations may be expected.

When an AI system is based on ML, you should generally make users aware of factors that may affect the accuracy of its predictions, such as the number of cases used to train the model, or the specific features that have the most influence over its predictions.

When an AI application relies on personal data, such as facial recognition system that takes images of people to recognize them, you should make it clear to the user how their data is used and retained, and who has access to it.

#### Accountability

People should be accountable for AI systems. Although many AI systems seem to operate autonomously, ultimately it's the responsibility of the developers who trained and validated the models they use, ad defined the logic that bases decisions on model predictions to ensure that the overall system meets responsibility requirements.

## Exercise: Prepare for an AI development project

1. You can access Azure AI Foundry portal directly at https://ai.azure.com. You will need to use your Azure credentials. You will be able logged into your default Azure default directory, but you will be able to switch to the appropriate directory by clicking on your profile icon.

2. An Azure AI project provides a workspace for AI development. You typically start by choosing a model that you want to work with and creating a project to use it.

| NOTE: |
| :---- |
| Remember that AI Foundry projects can be based on an Azure AI Foundry resource (which provides access to AI models, Azure AI services, and other resources for developing AI agents and chat solutions) or alternatively it can be based on AI hub resources (legacy). While the latter was intended for enterprise development teams, their use is currently discouraged. |

3. In the "Search Models" section, look for `o4-mini` and then click on "Use this Model".

4. Enter a valid name for your project and expand "Advanced options" to customize some of the settings. You will need to select the appropriate subscription, give a name to the resource group, and select the appropriate region.

| NOTE: |
| :---- |
| Some Azure AI resources are constrained by regional model quotas. You might be forced to create another resource in a different region if the model you intend to use is unavailable. |

5. Click "Create" and wait for the project to be created. You might be prompted to select the deployment model. By default, you should choose "Global standard" and customize the deployment details with a "Tokens per minute rate limit" of 50K (or the maximum). If not prompted, you will be able to see/edit this settings by clicking on "My Assets" &raquo; Models + Endpoints.

| NOTE: |
| :---- |
| Reducing the TPM helps avoid over-using the quota available in the subscription you are using. 50K is a sensible starting point. |

6. When your project is created, the chat playground will be opened automatically, so that you can test your model.

7. You can review your project by clicking on the left hand side navigation panel and selecting "Overview".

8. You can configure settings for the resource and the project by selecting the "Management center". The "resource" level information includes connectivity to Azure AI Services and Azure AI Foundry models and provides a central place to manage users and connections to Azure AI services at the resource level. The project level relates to this particular individual project.

9. Navigate the "resource" level overview and click on the "resource group" link to navigate to the resource definition in Azure. A new tab will be opened with the Azure Portal view of the resource group. In this screen you will be able to see the different Azure resources that has been created to support your Azure AI Foundry project. Initially it will show two resources, one of type Azure AI Foundry, and another of type Azure AI Foundry project.

10. Navigate back to Azure AI Foundry portal &raquo; Management Center page. In there click on "Go to Project".

11. In the project "Overview" page, there's a panel with the "Endpoints and keys" section. These are the endpoints and authorization keys you need to use in your application code to access:
    + The Azure AI Foundry project and any models deployed in it.
    + Azure OpenAI in Azure AI Foundry models.
    + Azure AI services.

12. Click on "Playgrounds" in the navigation pane, and open the "Chat Playground".

13. In the setup pane, is where you can give the model instructions and context. Here is where you can configure how the model should behave:

    ```
    You are a history teacher who can answer questions about past events all around the world.
    ```

14. In the chat window, you can enter a query:

    ```
    What are the key events in the history of the village "Luengos de los Oteros" in Santas Martas, province of Leon, Spain?
    ```

15. If everything goes well, after a few seconds (30 or so) you will get your response.

16. Once finished, navigate to the recently created resource group where you deployed the resources and click on "Delete resource group". This will endure that it won't incur in additional charges.