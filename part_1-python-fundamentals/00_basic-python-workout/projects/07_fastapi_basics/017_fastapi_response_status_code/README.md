# 017: Hello, FastAPI Response status code
> Illustrates the basics of FastAPI response status code

## Project description

You can declare the response status code of a path operation using the `status_code` parameter in your path operation decorator

### Returning a 201 from your POST path operation

Create a path operation for `POST /items/` that returns a 201 instead of the default 200.

As the parameter takes an `IntEnum`, create a `POST /v2/items` and `POST /v3/items` that returns a 201 using both `http.HTTPStaus` and `fastapi.status`.

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
