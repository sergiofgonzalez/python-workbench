# 004: Hello, Pydantic responses
> Illustrates how to use Pydantic to give structure to the agent's response

## Project description

Illustrates how to use Pydantic and the `response_format` parameter to force the agent to return the results in a predefined structure.

### Lab 1: Defining a Pydantic response model

Use Pydantic V2 to create an agent that responds to a user's request.

The user will type a question such as "What is the capital of the moon?", and the agent must make up a response with its name, location, vibe, and economy details.


## Running the program

You can run the application with:

```bash
uv run python main.py
```

## Project management

This project is managed using `uv`.
