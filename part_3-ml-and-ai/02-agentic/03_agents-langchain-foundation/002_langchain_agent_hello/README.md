# 002: Hello, LangChain Agent
> Illustrates how to create a basic agent using LangChain

## Project description

Illustrates how to create an agent with LangChain.

### Lab 1: Creating an agent

Create a function `hello_agent()` that performs the following:

Create an agent by invoking the function `create_agent(model="model")`.

This time, use claude-sonnet-4-5 and see what changes you need to apply.

Because you will be using LiteLLM as a provide, you will have to set the following environment variables (see `example.env`):

- api_key=os.environ["LITELLM_API_KEY"]
- base_url=os.environ["LITELLM_BASE_URL"]

If you were using OpenAI directly, it'd be enough to define an environment variable named `OPENAI_API_KEY`.

Then, to interact with the agent, use the `invoke()` method, taking into account that you will have to provide a dictionary which must include a `messages` key. In this simple case, the value for that key with be a list with a singular message of type `HumanMessage(content="the content")`.

Right after that, print the response from the message.

To simplify the user interaction, print the content of the last element of `messages`.

### Lab 2: Tampering with the agent's messages

Create a function `tampering_with_agent_messages()` in which you tamper with the response provided by the agent (supplanting what the agent has answered).

For example, you can do:

- Human: What is the capital of the Moon?
- AI (tampered): The capital of the Moon is Luna city.
- Human: Interesting. Can you tell me more about Luna city?

Check that the agent's response is always the last item of the `messages` value of the dictionary.


### Lab 3: Managing agent's latency

To reduce the perceived agent's latency, LangChain allows you to stream the agent's response.

For that, instead of invoking `agent.invoke()`, you can do something like (Note: actual code will require some additional fine-tuning to deal with proper type hints):

```python
for token, metadata in agent.stream({"messages": [HumanMessage(...)]}):
    if token.content:
        print(token.content, end="", flush=True) # print tokens as they arrive
```


## Running the program

You can run the application with:

```bash
uv run python main.py
```

## Project management

This project is managed using `uv`.
