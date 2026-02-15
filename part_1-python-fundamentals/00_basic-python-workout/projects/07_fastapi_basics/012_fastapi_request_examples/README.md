# 012: FastAPI: adding request and field examples
> Illustrates how to add request and field examples

## Project description

FastAPI supports adding examples in your model and parameter declaration (path, body, query, ...)

### Examples in Pydantic models

Create a path operation for `POST /items/{item_id}` where the endpoint accepts an Item model featuring:
+ `name`: required string
+ `description`: optional string
+ `price`: required float
+ `tax`: optional float

Include a couple of examples in the Pydantic model using `model_config.json_schema_extra.examples` array and see how it is showing in the `/docs`.

### Examples in Fields

Create a path operation for `POST /v2/items/{item_id}` where the endpoint accepts an Item model featuring:
+ `name`: required string
+ `description`: optional string, **examples given** for the field: "A very nice item"**
+ `price`: required float
+ `tax`: optional float

Check how it is showing in the `/docs`.

SOLUTION:

The example is shown in the Example textbox for the Response.

### Examples in Body

Create a path operation for `POST /v3/items/{item_id}` where the endpoint accepts an Item model featuring:
+ `name`: required string
+ `description`: optional string
+ `price`: required float
+ `tax`: optional float

In the path operation, give a couple of examples for the `Body` parameter.

Check how it is showing in the `/docs`.

### OpenAPI-specific examples

Create a path operation for `POST /v4/items/{item_id}` where the endpoint accepts an Item model featuring:
+ `name`: required string
+ `description`: optional string
+ `price`: required float
+ `tax`: optional float

In the path operation, give a couple of OpenAPI examples for the `Body` parameter. Please note that the shape of OpenAPI specific examples is different, with each example looking like the following:

```json
"normal": {
    "summary": "A normal example",
    "description": "A **normal** item works correctly.",
    "value": {
        "name": "Foo",
        "description": "A very nice Item",
        "price": 35.4,
        "tax": 3.2
    }
}
```

Check how it is showing in the `/docs`.

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
