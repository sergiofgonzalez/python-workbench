# 039: Hello, JSON lines streaming
> Illustrates how to stream JSON lines from FastAPI

## Project description

From v0.134, FastAPI supports streaming JSON lines. This project illustrates how.

### Returning a sequence of items as JSON lines

1. Start by creating a Pydantic model for an item, with name and optional description.

1. Create a list of items.

1. Define a path operation for `GET /items/stream` that returns your items as a stream of JSON lines asynchronously.

1. Define a path operation for `GET /items/stream` that returns your items as a stream of JSON lines synchronously.

SOLUTION:

You can test with:

```bash
# explicit use of streaming
$ http --stream :5000/items/stream-sync --verbose

# regular requests work too
$ http --stream :5000/items/stream-sync --verbose

```

## Running the program

You can run the application with:

```bash
uv run fastapi dev main.py --port {port}
```

## Project management

This project is managed using `uv`.

FastAPI dependency was added using:

```bash
$ uv add fastapi[standard-no-fastapi-cloud-cli]
```

as I don't intend to use FastAPI cloud at the moment.

The only other dependency was ruff:

```bash
$ uv add ruff --dev
```
