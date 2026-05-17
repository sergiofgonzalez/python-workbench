# 003: Cognee comprehensive demo using AzureOpenAI
> A comprehensive Cognee demo with AzureOpenAI models

## Project description

The demo illustrates how to create a kg with different sources and query all the given information as a whole.

There's a bug in Cognee and the graphs were not being saved in the directory. Claude had to modify Cognee's code to make it work.

## Running the program

Configure the `.env` following the template given in `.env.example`.

You can run the application with:

```bash
uv run python main.py
```

## Project management

This project is managed using `uv`.
