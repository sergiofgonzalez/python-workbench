# 028: Hello, FastAPI decorator dependencies
> Illustrates the basics of FastAPI dependencies in decorators

## Project description

If you're interested in invoking a dependency just for their side effects, you can include it in the path operation decorator, instead of in the path operation itself.

That way, they will be invoked, but the return value of those dependencies won't be passed to your path operations.

### Including dependencies on the path operation decorator

Create a path operation for `GET /items/` in which you first check that the value of the header `X-Token` and header `X-Key` is a particular one.

If that value is not found in any of the headers, an HTTP 400 should be returned.

SOLUTION:

This can be tested with:

```bash
$ http :5000/items/ X-Token:"fake-secret-token" X-Key:fake-secret-key
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
