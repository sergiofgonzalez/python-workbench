# 005: Hello, FastAPI request body
> Illustrates the basics of FastAPI request body management

## Project description

This lab illustrates several basic features of FastAPI with respect to request body management.

The request body allows you to send data from a client, but clients do not necessarily need to send request bodies.

| NOTE: |
| :---- |
| According to the specs, request bodies are available for `POST`, `PUT`, `DELETE`, and `PATCH`. Sending a request body in a `GET` response is undefined and you should not use it. |

In FastAPI request bodies are primarily defined with Pydantic models.

### Your first request body for a `POST` request

Create a program with a path operation for `POST /items/`. The path operation expects an `Item` object with the following fields:
+ `name`: required, string field.
+ `description`: optional, string field.
+ `price`: required, float field.
+ `tax`: optional, float field.

The implementation of the path operation should simply return the item.

Test the implementation using HTTPie using both a valid and invalid request body. What error code do you get when sending an invalid body?

Open the `/docs` endpoint and browse how the model definition has been included in the OpenAPI spec.

Does the path operation allows you to send fields in the request body not declared in the Pydantic model?

SOLUTION:
+ When you don't send the request body, you get an HTTP status code 422 telling you that the body is missing:

    ```json
    {
        "detail": [
            {
                "input": null,
                "loc": [
                    "body"
                ],
                "msg": "Field required",
                "type": "missing"
            }
        ]
    }
    ```

+ When sending a valid request body, with only the required fields, the request is successful:

    ```bash
    http POST localhost:5000/items/ name=iPhone price=99
    ```

    ```json
    {
        "description": null,
        "name": "iPhone",
        "price": 999.0,
        "tax": null
    }
    ```

+ When sending the full set of fields, the request is also successful:

```bash
http POST localhost:5000/items/ name=iPhone price=999 \
  description="the latest iPhone model at an unbeatable price" \
  tax=120
```

```json
{
    "description": "the latest iPhone model at an unbeatable price",
    "name": "iPhone",
    "price": 999.0,
    "tax": 120.0
}
```

+ When sending additional fields, those are accepted (they don't make the request fail), but ignored.

    ```bash
    $ http POST localhost:5000/items/ name=iPhone price=999 description="the latest iPhone model at an unbeatable price" tax=120 discount=0.15
    ```

    ```json
    {
        "description": "the latest iPhone model at an unbeatable price",
        "name": "iPhone",
        "price": 999.0,
        "tax": 120.0
    }
    ```

### Mixing a request body with path and query parameters

Request body objects can be used in path operations featuring path and query parameters. FastAPI will identify as query parameters those using a singular type (e.g., `int`, `float`, `str`, `bool`, ...).


Create another path operation for `PUT /items/{item_id}` that besided the `{item_id}` path parameter include an optional `q` query parameter.

In the implementation, return a dictionary with the field:
+ `item_id`
+ the fields and values from the request body object as a dictionary
+ the `q` query parameter if given

Test it with HTTPie.

SOLUTION:

```bash
http put localhost:5000/items/123 name=iPhone price=999 \
  description="the latest iPhone model at an unbeatable price" \
  tax=120 \
  q==query_string
```

```json
{
    "description": "the latest iPhone model at an unbeatable price",
    "item_id": 123,
    "name": "iPhone",
    "price": 999.0,
    "q": "query_string",
    "tax": 120.0
}
```

### Using the model as a Python object

Within the path operation, you can work with the request body model as if it were a regular Python object / dataclass.

Create a path operation for `POST /v2/items/` in which you return the model received as a dictionary, enhanced with a field `price_with_tax` which should have the value of the item's price + item's tax if present.

Test it with HTTPie.

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
