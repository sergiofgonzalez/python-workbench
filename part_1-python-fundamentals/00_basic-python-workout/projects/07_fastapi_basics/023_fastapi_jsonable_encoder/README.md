# 023: Hello, FastAPI  jsonable encoder
> Illustrates the basics of FastAPI's jsonable encoder

## Project description

`jsonable_encoder()` allows you to convert any datatype to a JSON compatible representation.

### Using `jsonable_encoder()`

Create a FastAPI application that features an `Item` model with fields:
+ title: required str
+ timestamp: required datetime
+ description: optional str

Create a path operation `PUT /items/{item_id}` in which you upsert the received item in a dict object `fake_db` using `item_id` as the key, and the JSON representation of the object as the value.

Inspect the contents of `fake_db`.

SOLUTION:

You can test it with:

```bash
$ http put :5000/items/foo title=foo description="foo description" timestamp="2026-02-18T08:51+02:00"
```

You can see that when the item is received, you have:

```python
datetime.datetime(2026, 2, 18, 8, 54, tzinfo=TzInfo(7200))
```

but in the fake db it gets stored as:

```python
'2026-02-18T08:51:00+02:00'
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
