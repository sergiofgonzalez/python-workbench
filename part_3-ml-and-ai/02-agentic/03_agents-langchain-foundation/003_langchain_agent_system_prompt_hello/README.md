# 003: Hello, LangChain Agent System Prompt
> Illustrates the basics of configuring a system prompt for your agent

## Project description

Illustrates different ways to configure an agent's system prompt to tailor how an agent responds.

### Lab 1: Configuring a system prompt for your agent

Build a sci-fi agent that is configured with the following system prompt:

```
You are a science fiction writer, create a capital city at the users request.
```

Check that the response is tailored to the system prompt instructions.


### Lab 2: Fine-tuning the system prompt

Build on the previous exercise to fine tune the system prompt by giving a few examples, similar to:

```
You are a science fiction write, create a capital city at the users request.

User: What is the capital of Mars?
Scifi Writer: Marsialis

User: What is the capital of the Moon?
Scifi Writer: Luna city
```

## Running the program

You can run the application with:

```bash
uv run python main.py
```

## Project management

This project is managed using `uv`.
