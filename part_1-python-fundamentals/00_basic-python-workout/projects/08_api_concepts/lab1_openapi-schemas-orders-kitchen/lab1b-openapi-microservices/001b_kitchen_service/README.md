# 001b: Kitchen service (with fake in memory db)
> A basic Kitchen service built from an OpenAPI schema

## Project description

This project provides a basic implementation of a basic orders service corresponding to [Lab 1.b](../../../README.md#lab-1b-implement-orders-service-according-to-the-openapi-schema-document).


### Application specs

This service has been

Additionally, the following details have been considered:
1. When listing orders, we want to return objects with the shape:

    ```json
    {
      "schedules": list_of_schedules
    }
    ```

1. You should not allow additional fields in the payloads, or additional query parameters.


Finally, wire your manually created OpenAPI schema document to your FastAPI program and adjust it as necessary so that it matches the implementation (in terms of behavior, you can leave out the documentation differences).

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

PyTest (+ `pytest-sugar` + `pytest-cov`) and Ruff were also added as dev dependencies:

```bash
$ uv add fastapi[standard-no-fastapi-cloud-cli] --dev
```
