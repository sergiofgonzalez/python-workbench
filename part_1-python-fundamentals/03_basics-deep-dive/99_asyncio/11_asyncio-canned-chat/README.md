# asyncio chat

## Setting up shop

The project was created using:

```bash
$ uv init 11_asyncio-canned-chat
```

The [`pyproject.toml`](pyproject.toml) was customized to use [Ruff](https://docs.astral.sh/ruff) linter.

## Description

Illustrates the simplest asyncio socket server and client that communicate via streams. The message the client sends is hardcoded, and the server sends back the same message received from the client, but in uppercase.