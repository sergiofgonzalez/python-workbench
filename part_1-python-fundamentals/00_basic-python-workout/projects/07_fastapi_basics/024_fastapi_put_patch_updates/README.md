# 024: Hello, PUT and PATCH updates with FastAPI
> Illustrates how to use PUT and PATCH for updates

## Project description

Illustrates how to do full updates with `PUT` and partial updates with `PATCH` when using FastAPI and Pydantic models.

### A simple FastAPI application with partial and full updates

Create a simple FastAPI application supporting full and partial updates.

Start by creating a Pydantic model representing an Item with the following fields:
+ name: optional str
+ description: optional str
+ price: required float
+ tax: optional float, default value 10.5
+ tags: optional list of strs, default the empty list

Then create the following list of items, simulating the information you'd typically keep in a DB:

```python
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}
```

Then, create a path operation that returns an item by its ID.

Afterwards, define an operation that performs the full update of the item using `PUT`. In the implementation you should:
1. Transform the model received into a JSON-compatible Python object (to store in `items`).
1. Update the given item in the fake db.
1. Return the item using the JSON-compatible representation.

Finally, define an operation that performs the partial updates using `PATCH`. The idea is that you'd receive an `Item` instance in which only the fields that need to be updated are present. In the implementation you should:
1. Read the existing data from the fake database
1. Re-hidrate the model from the data retrieved from the db
1. Transform the model received into a dict in which only the values that have been set are present.
1. Create an updated item, in which from the stored model, you perform the update of only the fields that have been sent in the request.
1. Update the fake database by creating a JSON-compatible representiation of the updated item.

| NOTE: |
| :---- |
| The `Item` features a lot of optional fields (e.g., name) to allow for this partial updates. |

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
