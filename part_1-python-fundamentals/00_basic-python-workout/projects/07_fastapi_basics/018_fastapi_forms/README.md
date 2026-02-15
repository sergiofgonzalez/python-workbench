# 018: Hello, forms with FastAPI
> Illustrates the basics of forms with FastAPI

## Project description

FastAPI provides `Form()` when you need to work with form fields instead of JSON.

| NOTE: |
| :---- |
| To use forms, you must first install [python-multipart](https://github.com/Kludex/python-multipart). |

### Using `Form()` parameters in the path operation

Create a path operation for a `POST /login/` form containing the fields:
+ username: required str
+ password: required str

In the implementation of the coroutine, return the dictionary `{"username": username}`.

### Using form models

Create a path operation for a `POST /v2/login/` form containing using a Pydantic model `FormData` containing the fields:
+ username: required str
+ password: required str

In the implementation of the coroutine, return the instance of the `FormData` instance.

### Forbidding extra fields

Create a path operation for a `POST /v3/login/` form containing using a Pydantic model `FormData` containing the fields:
+ username: required str
+ password: required str

Configure the model to forbid extra fields.

In the implementation of the coroutine, return the instance of the `FormData` instance.

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
