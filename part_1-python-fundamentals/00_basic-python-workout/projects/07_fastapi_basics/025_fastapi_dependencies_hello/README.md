# 025: Hello, FastAPI Dependency Injection
> Illustrates the basics of FastAPI Dependency Injection

## Project description

This project illustrates the most basic (and probably not very useful) usage of FastAPIs dependency injection system.

In the example, a common dependency consisting in returning certain parameters is used in several path operations.

### Dependency Injection 101

Create a coroutine `common_parameters()` (the dependency) that takes as parameters:
+ q: an optional string
+ skip: an optional int, with default value 0
+ limit: an optional int, with default value 100

Then, in the dependency implementation, return a dict with those values.

Then declare two path operations for `GET /items/` and `GET /users/` both of which depend on `common_parameters()`. Within the implementation, return the values provided by the common dependency.

Once validated, create a type alias to remove further duplication.

Check that OpenAPI /docs are correctly updated.

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
