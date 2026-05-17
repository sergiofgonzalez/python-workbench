# 006: Hello, short-term memory for LangChain agents
> Illustrates how to enable short-term memory in LangChain agents

## Project description

Illustrates how to use short-term memory when working with LangChain agents.

### Lab 1: no-memory agents

Confirm that LangChain agents keep no recollection of previous memories by creating an agent and interacting with it by saying:

Human: Hi, I'm Sergio and my favorite color is blue.
AI Message: ...
Human: Who am I and what's my favorite color?
AI Message: ...

Note that you shouldn't be appending the second human message to the conversation.

### Lab 2: Create an agent with short-term memory

Create an agent with short-term memory by initializing it with a checkpointer. Use, `langgraph.checkpoint.memory.InMemorySaver()` for simplicity.

Also, when invoking the agent, make sure apart from the messages, you pass a config object configured with a conversation id:

```python
config = {"configurable": {"thread_id": "1"}}
```

The thread_id will group all those checkpoints so that they stay together.

Repeat the exercise 1.

## Running the program

You can run the application with:

```bash
uv run python main.py
```

## Project management

This project is managed using `uv`.
