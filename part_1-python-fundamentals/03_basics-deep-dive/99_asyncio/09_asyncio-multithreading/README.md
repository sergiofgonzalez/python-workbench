# asyncio: executors and multithreading

This example illustrates how you can send a synchronous long running blocking work to a separate thread to prevent blocking the thread in which the event loop is running.

## Setting up shop

The project was created using:

```bash
$ uv init 09_asyncio-multithreading
```

The [`pyproject.toml`](pyproject.toml) was customized to use [Ruff](https://docs.astral.sh/ruff) linter.
