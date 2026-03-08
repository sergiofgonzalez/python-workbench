# 041: Hello, FastAPI testing (without /test dir)
> Illustrates the basics of FastAPI testing without /test dir

## Project description

Using `TestClient` test you can easily use [pytest](https://docs.pytest.org/) to test your FastAPI application.

This project demonstrate how to use `TestClient` in a project where your tests are hosted in files saved in the same directory as the modules their tests.

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── test_main.py
...
```

### Using `TestClient` for testing a simple app

1. Set up the structure of the "bigger application" with an `app` package (as illustrated above).

1. Define a `fake_secret_token`, that you'd use to validate the requests.

1. Define a `fake_db` with a dictionary of items with `id`, `title`, and `description`. Each of the items are indexed by their `id`.

1. Define an `Item` model with `id`, `title`, and optional `description`.

1. Declare a path operation for `GET /items/{item_id}`. In the path operation, you should accept the path parameter and an `X-Token` header.

    If the X-Token is not received, or if it's different from the value defined, raise a 400 error with the detail "Invalid X-Token header".

    If the `item_id` is not in the `fake_db` return a 404 with detail "Item not found".

    Otherwise, return the item as an `Item` model.

1. Declare a path operation for `POST /items/`. The operation should accept an `Item` in the request body and the `X-Token` in the header.

    If the X-Token is not received, or if it's different from the value defined, raise a 400 error with the detail "Invalid X-Token header".

    If the `item_id` is in the `fake_db` return a 409 with detail "Item already exists".

    Otherwise, return the item as an `Item` model.

1. Create a file `test_main.py`, and write the following tests using `TestClient` (note that `TestClient` is defined once per test file):

    1. Write the happy path for `GET /items/foo".
    1. Write the negative scenario when sending bad tokens to `GET /items/foo".
    1. Write the negative scenario for nonexistent item to `GET /items/foo".
    1. Write the happy path for `POST /items/".
    1. Write the negative scenario when sending bad tokens to `POST /items/".
    1. Write the negative scenario for duplicated item to `POST /items/".


## Running the program

You can run the application with:

```bash
uv run fastapi dev main.py --port {port}
```

## Running your tests

You can run the tests from your IDE or from the command line using:

```bash
uv run pytest
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
