# 008: Hello, FastAPI query parameter models
> Illustrates how to use Pydantic models for query parameters

## Project description

If you have a group of related query parameters, using Pydantic models will let you centralize the validations and documentation in a single place.

### Using a Pydantic model for the searching / sorting needs of your APIs

Create a Pydantic model `FilterParams` for your searching and sorting needs of your API. It must feature the following fields:
+ `limit`: integer field, with a default value of 100, and range between 0 and 100 (included).
+ `offset`: integer field, with a default value of 0, and must be greater than or equual to 0.
+ `order_by`: literal that could be either "created_at" or "updated_at". Default value is "created_at".
+ `tags`: list of strings, default value is empty array.

Then define a path operation for `/items/` that returns the query.

HINT: Pydantic metadata is declared using `Field`. Literals are declared using `typing.Literal`.

SOLUTION:
This can be tested in HTTPie with the following:

```bash
$ http :5000/items/ limit==1 offset==2 order_by==created_at tags==tag1 tags==tag2
```

### Preventing extra fields in the query parameter

Create a `FilterParamsV2` which prevents extra fields to be sent in the query parameters. Define a `/v2/items/` and validate that a request fails when sending extra params.


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
