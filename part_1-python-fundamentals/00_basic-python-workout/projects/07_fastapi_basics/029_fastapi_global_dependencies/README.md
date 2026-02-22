# 029: Hello, FastAPI global dependencies
> Illustrates how to set up dependencies for all the path operations

## Project description

Global dependencies (dependencies passed to the `FastAPI()` invocation) are applied to all the path operations in your application.

### Applying token validation and key validation for all the path operations

Create a couple of dependencies to validate that the contents of a fake X-Token and X-Key headers match the expectations (failing otherwise), and apply them globally to your app.

Validate that they are applied to multiple endpoints.

SOLUTION:

You can test it with:

```bash
$ http :5000/users/ X-Token:fake-secret-token X-Key:fake-secret-key
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
