# 007: Numeric validations on path parameters
> Illustrates how to apply numeric validations to path parameters

## Project description

This project illustrates how to do numeric validations on path parameters. Similar capabilities are available for other types (e.g., string) and other concepts (query parameters, headers, request bodies, cookies, ...).

### Path parameters and numeric validations

Create a path operation for a `GET /items/{item_id}` including an optional query parameter `q` aliased to `item-query`, and making `{item_id}` a numeric path parameter with title "Item ID", and greater or equal than 1.

Then include another query parameter `pct_discount` which should be a float between 0 and 100 (both included).

Test it with HTTPie and review the `/docs`.

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
