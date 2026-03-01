# 040: Hello, FastAPI's BackgroundTasks
> Illustrates the basics of FastAPI's background tasks

## Project description

FastAPI's `BackgroundTasks` lets you run activities after you've sent your response. This can be useful for logging, sending telemetry data, or to send lightweight notifications in the background once you're done with your path operation.

### Using `BackgroundTasks` as a path operation parameter

1. Create a `write_log()` coroutine that uses `aiofiles` to append to a file created in the same directory as the application named `log.txt`. In the implementation, the coroutine should write the same message it receives and prefixed by a timestamp.

1. Create a path operation for `POST /send-notification/{username}` that registers `write_log()` as a background task and then returns a response with a message and a timestamp.

Check that the timestamp in the log file is greater than the one in the response.

### Using `BackgroundTasks` with dependencies

1. Create a `get_query()` dependency that declares a query parameter `q`. In the implementation, if you have received `q` you should write a log message with the contents of the query parameter using a background task.

1. Create a path operation `GET /items/{item_id}` that declares `q` as a dependency and a `BackgroundTasks` parameter. In the path operation schedule writing the log with the item received and return the `item_id` received and the timestamp.

Confirm that both the dependency log info, and the path operation log info happen later than the timestamp in the response.

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
