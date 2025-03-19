# Harnessing the power of LLMs

LLMs and GPTs (Generative Pretrained Transformers) are generative models &mdash; they are trained to generate rather than predict or classify content.

The difference between generative and predictive models is that the former create something from the input, while the latter outputs the most probable class the phrase is aligned with.

An LLM is characterized by its constituent parts:
+ data &mdash; the content used to train the model itself
+ architecture &mdash; number of parameters, size of the model
+ training &mdash; the specific form of training used while building the model to identify its use case (chat, completions, instruction)
+ fine-tuning &mdash; the process of refininf the input data and model training to better match a particular use case or domain.

| NOTE: |
| :---- |
| ChatGPT is trained on the public Internet, and then fine-tuned using several training strategies. The final fine-tuning is completed using an advanced form called reinforcement learning with human feedback (RLHF). |

Chat completions LLMs are designed to improve through iteration and refinement (chatting). These models are also benchmarked against task completion, reasoning, and planning, which makes them ideal for building agents and assistants.

Completion models are trained/designed only to provide generated content on input text, so they don't benefit from iteration.

| NOTE: |
| :---- |
| For agents, you should focus on the class of LLMs called chat completion models. |

## Mastering the OpenAI API

The following section illustrates how to connect to an LLM model using the OpenAI Python SDK, which we'll connect to a GPT model. We'll see how to get the model response, count tokens, and how to define consistent messages.

| EXAMPLE: |
| :------- |
| See [01: Hello, OpenAI SDK](01-hello-openai-sdk/) for a runnable example illustrating how to interact with a chat completions LLM model hosted in Azure OpenAI using OpenAI SDK. |

### Connecting to the chat completions model

In the example [01: Hello, OpenAI SDK](01-hello-openai-sdk/), we first connect to a chat completions model o3-mini, which is hosted on Azure Open AI service. In order to do that, we need to instantiate a client:

```python
import os

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()


model_name = "o3-mini"
deployment = "o3-mini"
api_version = "2024-12-01-preview"

if not (subscription_key := os.getenv("AZURE_OPENAI_API_KEY")):
    msg = "Please configure your Azure OpenAI API key"
    raise ValueError(msg)

if not (endpoint := os.getenv("AZURE_OPENAI_ENDPOINT")):
    msg = "Please configure your Azure OpenAI endpoint"
    raise ValueError(msg)


client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)
```

You see that the important configuration pieces when interacting with a model hosted on Azure OpenAI are:
+ Azure Open AI endpoint
+ Azure Open AI API key
+ Azure Open AI API version

### Understanding the request and response

The request part in our example, looks like the following:

```python
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ],
    )
```

The request encapsulates the intended model, the messages, and sometimes the temperature.

Within the request, the most interesting part is the messages block. It describes the set of messages and roles used in a request.

Messages for a chat completions model can be defined in three roles:

+ System role &mdash; a message that describes the request's rules and guidelines. It is often used to describe the role of the LLM in making the request.

+ User role &mdash; represents and contains the message from the user.

+ Assistant role &mdash; can be used to capture the message history of previous responses from the LLM. It can also inject a message history when perhaps none existed.

```json
[
  { "role": "system", "content": "You are a helpful assistant." },
  { "role": "user", "content": "What is the capital of France?" },
  { "role": "assistant", "content": "The capital of France is Paris." },
  { "role": "user", "content": "What is an interesting fact of Paris?" },
]
```

When injecting that history, the response will look like the following:

```
ChatCompletion(
  id='chatcmpl-BAZfG0eyK3WQn8Acr8Ue9caP7xAK3',
  choices=[
    Choice(
      finish_reason='stop',
      index=0,
      logprobs=None,
      message=ChatCompletionMessage(
        content='...',
        refusal=None,
        role='assistant',
        annotations=None,
        audio=None,
        function_call=None,
        tool_calls=None),
      content_filter_results={
        'hate': {'filtered': False, 'severity': 'safe'},
        'protected_material_code': {'filtered': False, 'detected': False}, 'protected_material_text': {'filtered': False, 'detected': False},
        'self_harm': {'filtered': False, 'severity': 'safe'},
        'sexual': {'filtered': False, 'severity': 'safe'},
        'violence': {'filtered': False, 'severity': 'safe'}})
    ],
    created=1741860074,
    model='o3-mini-2025-01-31',
    object='chat.completion',
    service_tier=None,
    system_fingerprint='fp_ded0d14823',
    usage=CompletionUsage(
      completion_tokens=1280,
      prompt_tokens=64,
      total_tokens=1344,
      completion_tokens_details=CompletionTokensDetails(
        accepted_prediction_tokens=0,
        audio_tokens=0,
        reasoning_tokens=1152,
        rejected_prediction_tokens=0),
      prompt_tokens_details=PromptTokensDetails(
        audio_tokens=0, cached_tokens=0)),
    prompt_filter_results=[
      {
        'prompt_index': 0,
        'content_filter_results': {
          'hate': {'filtered': False, 'severity': 'safe'},
          'jailbreak': {'filtered': False, 'detected': False},
          'self_harm': {'filtered': False, 'severity': 'safe'},
          'sexual': {'filtered': False, 'severity': 'safe'},
          'violence': {'filtered': False, 'severity': 'safe'}}}
    ])
```

## Prompting LLMs with prompt engineering

A prompt defined for LLMs is the message content used in the request for better response output.

Prompt engineering is a new and emerging field that attempts to structure a methodology for building prompts.

Organization such as OpenAI have begun documenting a universal set of strategies coverting various tactics, some requiring additional infrastructure and consideration.

| Category | Strategy | Description |
| :------- | :------- | :---------- |
| Basics | Write Clear Instructions | Be specific in what you ask. Tactics include detailing queries, adopting personas, using delimiters, specifying steps, providing examples, and specifying output length. |
| Memory | Provide Reference Text | Help reduce fabrications by instructing the model to use or cite reference texts. |
| Memory | Use External Tools | Enhance model capabilities by using tactics such as include embeddings-based search, code execution, and access to specific functions. |
| Planning | Split Complex Tasks into Simpler Subtasks | Reduce error rates by using tactics such as intent classification, summarizing dialogues, and piecewise summarization of documents. |
| Planning | Give Models Time to "Think" | Allow more reliable reasoning by using tactics such as working out solutions before conclusions, using inner monologue, and reviewing previous answers. |
| Evaluation | Test Changes Systematically | Ensure improvements are genuine by evaluation model outputs with reference to standard answers. |

Examples of tactics:

1. Write Clear Instructions: Provide as much detail as you can in a query; generally the more detailed the better.

Who is the prime minister of Canada and how frequently are elections held?

2. Adopting Personas: Personas can include details about demographics, knowledge, and personality.

System: You are a prompt expert and will suggest ways to improve a user request.
User: What is the capital of Canada?

3. Using Delimiters: Delimiters can help separate blocks of content from specification details.

User: Summarize the text delimited by triple quotes with a limerick: '''text to be summarized'''

4. Specifying steps: using steps can help the LLM better process the task, but be sure to limit the number.

System: Use the following step-by-step instructions to respond to user inputs. Step 1: Summarize the text in triple quotes to one setence with a prefix that says "Summary". Step 2: Translates the summary from Step 1 into Spanish with a prefix that says "Translation".

User: '''text to summarize and translate'''

5. Providing examples: Examples are a form of few-shot learning and can be an excellent way to indicate the desired response format and other details.

System: Answer in a consistent style.

User: Teach me about patience.

Assistant: The river that carves the deepest valley flows from a modest spring; the most intricate tapestry begins with a solitary thread.

User: Teach me about the ocean.

6. Specify Output Length: Limiting the length of output can be specific to words, bullet points, or other metrics.

User: Summarizes the text delimited by triple quotes in about 50 words. '''text to summarize'''

## Choosing the optimal LLM for your specific needs

Being a successful consumer of AI agents doesn't require an in-depth understanding of LLMs, it's helpful to be able to evaluate the specifications.

Some fundamental dimensions to take into account:

1. **Model Performance**

    Determines how well a model performs given a certain benchmark such as answering SAT questions.
    You should measure the performance in the context of the use case you're building. For example, if you're building a coding related use case, an LLM that performs well on code is essential.

2. **Model Parameters/Model Size**

    The number of billions of parameters of the model. Larger models perform better on general tasks as it is related to how well the model will be able to perform inference. A larger model will require more infrastructure to run.


3. **Use Case/Model Type**

    Determines the type of model and expected use case. This could be chat completions for a model such as ChatGPT, which is good for iterating and reasoning through a problem.
    There are also models good for question/answer, and instruction-based.
    In general, agent applications work well with chat completions models.


4. **Training Input**

    Specifies the material used to tran the model. This can change from everything found on the Internet to a specific domain Python code.

5. **Training Method**

    Specifies how the model is trained and/or fine-tuned. Models like ChatGPT are trained using reinforcement learning with human feedback.



6. **Context Token Size**

    Specifies how large the model's context size is in tokens. Larger context is important for verbose agent conversations.
    A context window of about 4,000 tokens is generally enough for simple tasks. However, a large context window can be beneficial when using multiple agents that share a common context.

7. **Model Speed/Model Deployment**

    Denotes the speed of the model. OpenAI models marked Turbo are typically faster. For local LLMs speed is determined by the infrastructure in which they are hosted.
    When you're interacting with users, real-time speed might be required.


8. **Model Cost**

    Could represent the price of the service or the cost to host and run a model on your infrastructure.


## Exercises

### Exercise 1: Consuming LLMs

Create a program that uses the same prompt with at least two different LLMs and compare the results.

See [e01: Consuming LLMs](e01-comparing-llms/)
