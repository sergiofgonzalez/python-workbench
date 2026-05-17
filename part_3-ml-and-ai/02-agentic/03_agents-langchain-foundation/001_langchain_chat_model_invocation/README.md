# 001: Hello, Chat Model Invocation using LangChain
> Illustrates the basics of invoking a chat model using LangChain.

## Project description

Illustrates the basics of invoking a chat model using LangChain and getting a response.

### Lab 1: invoke a model and print the response

Create a function `invoke_model_bare()` that uses `init_chat_model()` to instantiate a `BaseChatModel` instance of `gpt-5-mini` using LiteLLM as the provider.

Because you will be using LiteLLM as a provide, you will have to set the following environment variables (see `example.env`):

- api_key=os.environ["LITELLM_API_KEY"]
- base_url=os.environ["LITELLM_BASE_URL"]

If you were using OpenAI directly, it'd be enough to define an environment variable named `OPENAI_API_KEY`.


Then, use the method `invoke()` with certain user input and print:

1. The `response` object (which should be an object of type `AIMessage`).

1. The field `content`, which should contain the response the user is waiting for.

1. The field `response_metadata` which should contain interesting information about the response (such as model used, total duration of the invocation, etc.)


### Lab 2: invoke the model adjusting the temperature

Repeat the previous exercise, but this time define a function `invoke_model_with_temp()` setting the model temperature to 1.0. Check if the answer is less deterministic.


## Running the program

You can run the application with:

```bash
uv run python main.py
```

## Project management

This project is managed using `uv`.
