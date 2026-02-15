# 013: Hello, FastAPI support for other data types (datetimes, uuids, etc.)
> Illustrates FastAPI support for other data types (datetimes, uuids, etc.)

## Project description

FastAPI provides support for some other datatypes for which you will find the same features (conversion, validation, ...) you find for `str` or `float` types.

### Path operation with extra data types

Create a path operation for `PUT /items/{item_id}` featuring the following path and body parameters:
+ path:
  + item_id: UUID, required
+ body:
  + start_datetime: required datetime
  + end_datetime: required endtime
  + process_after: required timedelta
  + repeat_at: optional time

In the path operation coroutine, implement the following logic:

1. Calculate the start_process datetime by adding `start_datetime` and `process_after`.

1. Calculate the duration by subtracting `end_datetime` from `start_process`.

1. Then return all the values from the path and body, as well as the `start_process` and `duration`.

SOLUTION:

This can be tested with:

```bash
# Using ISO8601 format for duration
$ http put :5000/items/12345678-1234-5678-1234-567812345678 start_datetime=2026-02-14T19:37+02:00 end_datetime=2026-02-14T20:37+02:00 process_after=PT60S

# Using number of seconds
$ http put :5000/items/12345678-1234-5678-1234-567812345678 start_datetime=2026-02-14T19:37+02:00 end_datetime=2026-02-14T20:37+02:00 process_after:=60.0
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
