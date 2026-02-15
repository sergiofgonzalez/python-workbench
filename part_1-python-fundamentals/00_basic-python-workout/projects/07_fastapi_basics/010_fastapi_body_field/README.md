# 010: Hello, Pydantic Field for request body parameters
> Illustrates the basics of Field for body parameters

## Project description

Validation and metadata for request body parameters is done through `pydantic.Field`.


### Using Field to add validation and metadata to body parameters

Create a path operation for `PUT /items/{item_id}` including:
+ A required request body model with fields:
  + name: required string
  + description: optional string, with title "Description of the item" and a maximum length of 300 chars.
  + price: required float, must be greater than zero and description "Item's price (must be greater than zero)".
  + tax: optional float
+ an int path parameter `item_id` with title "Item ID" whose value must be between 0 and 1000 (inc.).

In the path operation, return a dictionary with the elements received.


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
