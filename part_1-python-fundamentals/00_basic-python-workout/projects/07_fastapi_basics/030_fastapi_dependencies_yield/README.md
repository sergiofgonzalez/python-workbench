# 030: Hello, FastAPI dependencies with yield
> Illustrates how to implement dependencies with yield in FastAPI

## Project description

FastAPI supports a mechanism to allow dependencies to do some extra steps (called *exit code* or *exit logic*) after the request has been processed by FastAPI.

These dependencies need to use `yield` (only once per dependency), and write the *exit logic* after the `yield`.

| NOTE: |
| :---- |
| Those dependencies should be built as context manager/async context manager functions but without the decorator. |

This is quite an advanced topic, and it will be further elaborated on specific scenarios involving databases, etc.

### A simple yield dependency scenario involving exceptions

Dependencies with `yield` can implement try-except block. When doing so, caught exceptions should be typically re-raised or mapped to `HTTPExceptions`.

Create a program if which you define a fake items db with a few items featuring a `name` and an `owner`. Create a `get_username()` dependency using yield that yields a particular username (e.g., `scott`).

The dependency should implement except clauses for a custom `OwnerError` and `HTTPException`. In the first case, the exception should be mapped to an HTTP 400 (Bad Request). In the second, the error should just be logged and the `HTTPException` re-raised.

Then implement a path operation for `GET /items/{item_id}` in which:
+ if the item is not found in the db, a 404 HTTPException is raised.
+ if the item is found, but the item.owner does not match the value returned by `get_username()` an `OwnerError` is raised.`
+ if everything goes OK, the item is returned.


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
