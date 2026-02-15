# FastAPI
> a few misc notes and examples on FastAPI basics without minding much on web app concepts

+ [Before you begin with FastAPI](#before-you-begin-with-fastapi)
    + [A few words on Pydantic](#a-few-words-on-pydantic)
    + [Type hints in FastAPI](#type-hints-in-fastapi)
        + [Tech details](#tech-details)

+ [FastAPI basic concepts](#fastapi-basic-concepts)
    + [Running the examples](#running-the-examples)
    + [Installing FastAPI](#installing-fastapi)
    + [Hello, FastAPI](#hello-fastapi)
        + [OpenAPI](#openapi)
    + [Using path parameters](#using-path-parameters)
        + [Order declaration in path operations](#order-declaration-in-path-operations)
        + [Predefined values for your path parameters](#predefined-values-for-your-path-parameters)
        + [Path parameters containing paths](#path-parameters-containing-paths)
    + [Using query parameters](#using-query-parameters)
        + [Query parameter defaults](#query-parameter-defaults)
        + [Optional query parameters](#optional-query-parameters)
        + [Conversions for Boolean query parameters](#conversions-for-boolean-query-parameters)
        + [Multiple path and query parameters](#multiple-path-and-query-parameters)
        + [Required query parameters](#required-query-parameters)
        + [Putting it all together](#putting-it-all-together)
    + [Request body](#request-body)
        + [Using the model](#using-the-model)
    + [Query parameters and string validations](#query-parameters-and-string-validations)
        + [Query validation in older versions of FastAPI](#query-validation-in-older-versions-of-fastapi)
        + [Additional string validations](#additional-string-validations)
        + [Default values](#default-values)
        + [Required query parameters](#required-query-parameters-1)
            + [Required, can be `None`](#required-can-be-none)
        + [Query parameter list / multiple values](#query-parameter-list--multiple-values)
        + [Declaring additional metadata](#declaring-additional-metadata)
        + [Alias parameters](#alias-parameters)
        + [Deprecating parameters](#deprecating-parameters)
        + [Excluding parameters from OpenAPI](#excluding-parameters-from-openapi)
        + [Custom Validation](#custom-validation)
    + [Path parameters and numeric validations](#path-parameters-and-numeric-validations)
        + [Number validations](#number-validations)
    + [Query parameter models](#query-parameter-models)
        + [Forbidding extra query parameters when using Pydantic Models](#forbidding-extra-query-parameters-when-using-pydantic-models)
    + [Body: Multiple parameters](#body-multiple-parameters)
        + [Multiple body parameters](#multiple-body-parameters)
        + [Singular values in body](#singular-values-in-body)
        + [Multiple body and query parameters](#multiple-body-and-query-parameters)
        + [Embeddding body parameters](#embeddding-body-parameters)
    + [Body: Fields](#body-fields)
    + [Body: Nested models](#body-nested-models)
        + [List fields](#list-fields)
        + [Set field](#set-fields)
        + [Nested models](#nested-models)
        + [Special types and validation](#special-types-and-validation)
        + [Attributes with a list of submodels](#attributes-with-a-list-of-submodels)
        + [Deeply nested models](#deeply-nested-models)
        + [Bodies of pure lists](#bodies-of-pure-lists)
        + [Bodies of arbitrary dicts](#bodies-of-arbitrary-dicts)
    + [Declaring request example data](#declaring-request-example-data)
        + [`Field` examples](#field-examples)
        + [`Body` examples](#body-examples)
        + [OpenAPI-specific examples](#openapi-specific-examples)
    + [Extra data types you can use in FastAPI](#extra-data-types-you-can-use-in-fastapi)
    + [Cookie parameters](#cookie-parameters)
        + [Cookie parameter models](#cookie-parameter-models)
        + [Forbiding extra cookies](#forbidding-extra-cookies)
    + [Header parameters](#header-parameters)
        + [Duplicate headers management](#duplicate-headers-management)
        + [Header parameter models](#header-parameter-models)
        + [Forbidding extra headers](#forbidding-extra-headers)
        + [Disabling underscore conversions in header models](#disabling-underscore-conversions-in-header-models)
    + [Response model: return type](#response-model-return-type)
        + [The `response_model` Parameter](#the-response_model-parameter)
        + [Using the same model as the request and response model](#using-the-same-model-as-the-request-and-response-model)
        + [Using different models for request and response](#using-different-models-for-request-and-response)
        + [Return Type and Data Filtering](#return-type-and-data-filtering)
        + [Other return type annotations](#other-return-type-annotations)
        + [Invalid return type annotations](#invalid-return-type-annotations)
        + [Response model: excluding default values](#response-model-excluding-default-values)
        + [`response_model_include` and `response_model_exclude`](#response_model_include-and-response_model_exclude)
    + [Extra models](#extra-models)
        + [Declaring a response to be the union of two or more types](#declaring-a-response-to-be-the-union-of-two-or-more-types)
        + [Declaring a response to be a list of objects](#declaring-a-response-to-be-a-list-of-objects)
        + [Declaring a response to be an arbitrary dict](#declaring-a-response-to-be-an-arbitrary-dict)
    + [Response status code](Response status code)
        + [HTTP status codes](#http-status-codes)
    + [Form data](#form-data) -> 018:ready
        + [Form models](#form-models)
        + [Forbidding extra form fields](#forbidding-extra-form-fields)





## Before you begin with FastAPI
> prerequisites

### A few words on Pydantic

FastAPI is all based on Pydantic.

[Pydantic](https://docs.pydantic.dev/) is a Python library to perform data validation.

When using Pydantic, you declare the shape of the data as classes with attributes with their specific type.

Then, you create an instance of the class with some values and Pydantic will validate the values maybe converting them to the appropriate type (if needed) and hand over an object with all the data so that you can use it.

```python
from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = "Jason Isaacs"
    signup_ts: datetime | None = None
    friends: list[int] = []

external_data = {
    "id": "123", # id as string, not an int
    "signup_ts": "2026-02-05 13:24", # ts as str, not a datetime obj
    "friends": [1, "2", b"3"], # mix of things that can be converted to int
}

user = User(**external_data)
print(user)
print({user.id=}; ({type(user.id).__name__}))
```

### Type hints in FastAPI

FastAPI relies on type hints for:

+ **Define requirements**
    define requirements from request path parameters, query parameters, headers, bodies, dependencies, etc.

+ **Convert data**
    convert data from request to the required type.

+ **Validate data**
    validate data coming from each request and generating errors automatically and returning them to the client when the data is invalid without requiring additional logic from your side.

+ **Document the API using OpenAPI**
    which can then be used by automatic interactive documentation user interfaces.

### Concurrency and async / await

In a nutshell, you should follow this guidance given by FastAPI documentation:

1. If you're using async 3rd party libraries that you call using async / await, then declare your path operations as coroutines:

    ```python
    @app.get("/")
    async def read_results():
        results = await some_async_lib()
        return results
    ```

2. Instead, if you're using a 3rd party library that doesn't support async calls, declare your path operations as functions:

    ```python
    @app.get("/")
    def read_results():
        results = some_async_lib()
        return results
    ```

3. If you're not using any 3rd party library in your path operation (that is, only regular Python logic), use coroutines:

    ```python
    @app.get("/")
    async def home():
        return "you're home"
    ```

Note that in any case, FastAPI will still work asynchronously and be extremely fast.

Starlette (a FastAPI dependency) and FastAPI itself are based on [`AnyIO`](https://anyio.readthedocs.io/en/stable/), a library that enables async programming using both `asyncio` and [`Trio`](https://trio.readthedocs.io/en/stable/).

In particular, you can use AnyIO within your FastAPI apps for your more advanced async needs (e.g., structured concurrency).

#### Tech details

When you declare a path operation function (as opposed to a path operation coroutine), it is run in an external threadpool that is then awaited, instead of being called directly (to prevent blocking the server waiting for requests).

Because of this, if your path operation contains regular Python logic and do not perform any blocking I/O (e.g., calling a database or doing a file operation using non-asyncio libs), it's better to use coroutines.

The same applies for dependencies. If a dependency is a standard function (as opposed to a coroutine), it is run in the external threadpool.

You can also have sub-dependencies (i.e., 3rd party dependencies) requiring each other and mixing coroutines and regular functions in FastAPI. The ones created with functions would be called on an external thread from the threadpool instead of being awaited.

You will be responsible for managing the invocation of the utility functions that you call directly in your path operations (i.e., FastAPI won't do anything with that).

## FastAPI basic concepts

### Running the examples

To run FastAPI examples in development mode type:

```bash
fastapi dev main.py
```

### Installing FastAPI

To install FastAPI you will typically install `fastapi[standard]`. This comes with some default optional dependencies including `fastapi-cloud-cli` which you might not want.

If you don't want the optional dependencies, install `fastapi` instead. If you want the standard dependencies but without the cloud cli you can install `fastapi[standard-no-fastapi-cloud-cli]`.

| NOTE: |
| :---- |
| `fastapi` command is not included in `fastapi`: you should at least install `fastapi[standard-no-fastapi-cloud-cli]`. |

### Hello, FastAPI

The simplest FastAPI app is:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, world!"}
```

And can be executed in development mode running:

```bash
fastapi dev main.py
```

You will be able to point your browser to:
+ http://127.0.0.1:8000 to check your FastAPI app.
+ http://127.0.0.1:8000/docs to see the automatic interactive API documentation provided by SwaggerUI.
+ http://127.0.0.1:8000/redoc to see the automatic interactive API documentation powered by ReDoc

The important steps of the program are the following:

1. Import `FastAPI`: `FastAPI` is the Python class that provides all the functionality required to build your API.

    ```python
    from fastapi import FastAPI
    ```

1. Create a `FastAPI` instance.

    ```python
    app = FastAPI()
    ```

1. Create a **path operation**: because you're using *compute-only* logic in the implementation, you should follow the guidance and define the path operation as a coroutine:

    ```python
    @app.get("/")
    async def root():
        return {"message": "Hello, World!"}
    ```

    Note that *path* in this context refer to the last path of the URL staring from the first `/`. For example, on a site URL like `https://example.com/items/foo`, the path would be `/items/foo`. The path can also be referred to as *"endpoint"* or *"route"*.

    *Operation* in this context refers to the HTTP method that should be used to *activate* your coroutine (`GET` in this particular case).

1. The path operation is declared using a decorator. `@app.get("/")` tells FastAPI that the coroutine below will handle requests that go to the path `/` using an HTTP `GET` request.

    FastAPI defines decoractors for all the HTTP methods such as `@app.post()`, `@app.options()`, `@app.trace()`, etc.

1. Finally, you return the results of your path operation.

    You can return a `dict`, `list`, singular values such as `str`, `int`, etc. or Pydantic models represented more complicated data structures.

    All of them will be automatically converted to JSON.

| NOTE: |
| :---- |
| While this is explained on the Web Apps section, remember that <ul><li>POST: used to create data.</li><li>GET: used to read data.</li><li>PUT: used to update data.</li><li>DELETE: used to delete data.</li></ul> |

#### OpenAPI

FastAPI automatically generates a schema with all the APIs defined in your application using the OpenAPI standard for defining APIs.

This OpenAPI specification includes your API paths, possible paramters they take, etc.

OpenAPI defines an API schema for your API, and that schema includes definitions (or schemas) of the data sent and received by your API using JSON schema, the standard for JSON data schema definitions.

If interested, FastAPI automatically generates a JSON schema with the OpenAPI spec at http://127.0.0.1:8000/openapi.json.

### Using path parameters

Path parameters are variable parts of an URL path.

You can declare path parameters with the same syntax used by Python f-strings.

```python
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
```

In the example above, the value of the path parameter will be passed for the function/coroutine as the argument `item_id` (e.g., http://127.0.0.1/items/foo will make ´item_id="foo"`).

You can declare the type of a path parameter in the function/coroutine using standard Python type annotations:

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

If you hit http://127.0.0.1/items/3, FastAPI will make `item_id=3`.

However, if you hit http://127.0.0.1/items/foo, you will get an HTTP 422 error (Unprocessable Content) and the following error message signaling a validation error:

```python
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "watch"
    }
  ]
}
```

You'll get a similar error if you hit: http://127.0.0.1/items/3.14.

The automatic documentation will also be aware of your types, showing the expected type for the path parameter and the status codes (both for happy path and negative scenarios) that you might find.

#### Order declaration in path operations

You can find some situations where you have a fixed path such as `/users/me` and others such as `/users/{user_id}`.

In those case, FastAPI evaluates the paths in order, and you have to make sure that `/users/me` is declared before `/users/{user_id}` to prevent an HTTP 422 validation error to be returned.

```python
@app.get("/users/me")
async def read_user():
    return {"user_id": "current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```

If you declare the path operations in different order, the path for `/users/{user_id}` will be used for both `/users/me` and `/users/uid-012`.

Similarly, you cannot redefine a path operation:

```python
@app.get("/users")
async def read_users():
    return ["Alice", "Bob"]

@app.get("/users")
async def read_users2():
    return ["Charlie", "Darlene"]
```

The first operation will always be used.

#### Predefined values for your path parameters

If you have a path operation that receives a path parameter, but you want the possible valid path parameters to be amongst a given set of predefined values, you can use an `Enum`.

```python
# Enum mixin that forces Enum values to be string
class TeamName(str, Enum):
    ferrari = "ferrari"
    mclaren = "mclaren"
    aston_martin = "astonmartin"
    mercedes = "mercedes"
    red_bull = "redbull"

@app.get("/teams/{team_name}")
async def get_model(team_name: TeamName):
    if team_name is TeamName.ferrari:
        return {"team_name": team_name, "message": "for the win!"}

    if team_name.value == "astonmartin":
        return {"team_name": team_name, "message": "looking for some podiums!"}

    return {"team_name": model_name, "message": "championship contenders!"}
```

The values in the enum, will be considered in the OpenAPI spec, which will inform the user of the allowed values for that path parameter.

Note that when your return an enum member in your path operation, FastAPI will convert it to its corresponding value.

For example, if you hit `/teams/astonmartin` you will get the following JSON response:

```python
{
  "team_name": "astonmartin",
  "message":  "looking for some podiums!"
}
```

#### Path parameters containing paths

You might need define a path operation with a path such as `/files/{file_path}` (e.g., `/files/home/ubuntu/myfile.txt`).

While OpenAPI doesn't support declaring a path parameter that is path, you can do it in FileAPI using a path convertor:

```python
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
```

Note that if the path represents an absolute path:

```bash
$ http localhost:5000/files/myfile.txt
HTTP/1.1 200 OK

{
    "file_path": "myfile.txt"
}


$ http localhost:5000/files/home/ubuntu/myfile.txt
HTTP/1.1 200 OK

{
    "file_path": "home/ubuntu/myfile.txt"
}


$ http localhost:5000/files//home/ubuntu/myfile.txt
HTTP/1.1 200 OK

{
    "file_path": "/home/ubuntu/myfile.txt"
}
```

### Using query parameters

The query part of a URL is the set of key-value pairs that go after the `?`. Each key-value pair is separated by `&`.

When you declare other function/coroutine parameters that are not part of the path parameters, they are automatically interpreted as query parameters:

```python
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]
```

In the example above, hitting `/items/?skip=0&limit=10` will make:
+ `skip=0`
+ `limit=10`

FastAPI will also convert them to the type specified in the function/coroutine signature, raising an HTTP 422 (Unprocessable Content) error if that conversion doesn't succeed.

#### Query parameter defaults

As query parameters are not a fixed part of a path, they are optional and can have default values.

In the example above, hitting `/items/` would be the same as hitting `/items/?skip=0&limit=10`.

If you do `/items/?skip=20` would be the same as `/items/?skip=20&limit=10`.

#### Optional query parameters

You can declare an optional query parameter by setting its default to `None`.

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

In the example above, `q` is an optional query parameter, which will be `None` by default.

#### Conversions for Boolean query parameters

Consider the following snippet, which declares a boolean query parameter:

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "long desc for the item"})
    return item
```

FastAPI will set `short=True` in the following cases:
+ `/items/foo?short=1`
+ `/items/foo?short=True`
+ `/items/foo?short=true`
+ `/items/foo?short=on`
+ `/items/foo?short=yes`
+ any other case variation of the scenarios above

#### Multiple path and query parameters

You can declare multiple path parameters and query parameters in any order. FastAPI will know which is which:

```python
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_items(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "long desc for the item"})
```

Note that you will need to follow Python rules. For example, you cannot have parameters without default values after parameters with default values.

#### Required query parameters

If you want a query parameter to be required, declare it without any default value. FastAPI will then require that parameter to be always passed:

```python
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item
```

If you hit `/items/foo` you will get the following HTTP 422 (Unprocessable Content) error and the following error message:

```json
{
    "detail": [
        {
            "input": null,
            "loc": [
                "query",
                "needy"
            ],
            "msg": "Field required",
            "type": "missing"
        }
    ]
}
```

#### Putting it all together

FastAPI doesn't prevent you from having a path operation mixing the three types of query parameters:
+ optional query parameters: those with a default value set to `None` (e.g., `q: str | None = None`).
+ query parameters with default values: those with a default value other than `None` (e.g., `skip: int = 0`).
+ required parameters: those without a default value (e.g., `needy: str`)

```python
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str, skip: int = 0, limit: int | None = None):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item
```

In the snippet above:
+ `item_id` is a path parameter.
+ `needy` is a required query parameter.
+ `skip` is an optional query parameter with default value.
+ `limit` is an optional query parameter without default value.

### Request body

The request body allows you to send (somewhat complex) data from a client. Clients don't necessarily need to send request bodies. Sometimes it's sufficient to hit some path (e.g., `/items/`), with maybe some query parameters (e.g., `?skip=10&limit=10`).

| NOTE: |
| :---- |
| According to the specs, request bodies are available for `POST`, `PUT`, `DELETE`, and `PATCH`. Sending a request body in a `GET` response is undefined and you should not use it. |

On the other hand, your APIs will almost always send bodies to the client, these are known as response bodies.

To declare a request body, in FastAPI, you use Pydantic models:

```python
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
```

Note that:
+ `description` and `tax` are optional fields in the request body.
+ The request body is declared as the query parameters: as a function/coroutine paramter.

In turn FastAPI will do this for you:
+ Read the body of the request as JSON
+ Do the necessary conversion (if needed, although it's less common in request bodies).
+ Validate the data, raising an 422 error indicating where and why the validation failed.
+ Hand over the received information as a Python object (in this case, in `item`).
+ Generate JSON schema definitions for the model.
+ Include those definitions in the OpenAPI schema automatically.

There's no problem declaring both path parameters and a request body:

```python
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}
```

Or path parameters, query parameters, and a request body:

```python
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result
```

Please note that:
+ If a parameter is also declared as a path parameter, it will be used as a path parameter.
+ If the parameter is of singular type (e.g., `int`, `float`, `str`, `bool`, etc.) it will be interpreted as a query parameter.
+ If the parameter is a Pydantic model, it will be interpreted as a request body.

As you can see above, ordering of the parameters is unimportant.

#### Using the model

Inside the coroutine, you can work with the model as if it were a regular Python dataclass:

```python
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```

### Query parameters and string validations

FastAPI allows you to declare additional validation information for your parameters. For example, you might want a particular query parameter to be optional, but if provided, make sure its length doesn't exceed 50 chars.

```python
from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

`Annotated` is used to add metadata for the parameters. `Query` (from FastAPI) is used to provide additional information about the extra validations that should be performed on the query parameter.

| NOTE: |
| :---- |
| There are similar classes for `Path()`, `Body()`, `Header()`, and `Cookie()` in FastAPI. `Query` is specific to query parameters. |

#### Query validation in older versions of FastAPI

You may come across code using older versions of FastAPI in which `Annotated` was not used. The equivalent to `q: Annotated[str | None, Query(max_length=50)] = None` in those old versions was:

```python
@app.get("/items/")
async def read_items(q: str | None = Query(default=None, max_length=50)):
    ...
```

| NOTE: |
| :---- |
| Using `Annotated` is the recommended way in the modern versions of FastAPI. The code above is presented for illustration purposes only. |

#### Additional string validations

You can configure `Query` with the following validations:
+ `max_length`: maximum length of the parameter.
+ `min_length`: minimum length of the parameter.
+ `pattern`: to define a regular expression the parameter should match.

```python
@app.get("/items/")
async def read_items(q: Annotated[
    str | None,
    Query(min_length = 3, max_length=50, pattern=r"^fixedquery$")] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

#### Default values

You can declare default values other than `None`:

```python
@app.get("/items/")
async def read_items(q: Annotated[
    str | None,
    Query(min_length = 3)] = "fixedquery"
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

#### Required query parameters

A query parameter will be considered required if a default value for it is not provided:

```python
@app.get("/items/")
async def read_items(q: Annotated[str, Query(min_length = 3)]
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

##### Required, can be `None`


It is possible to declare a query parameter as required, but that can accepts `None`. That is, the client is forced to send a value, but that value can be `None`.

| NOTE: |
| :---- |
| This seems to be an edge case, which is quite difficult to test and find a scenario in which it would be useful. |

To do so, you just need to declare the type as `str | None` without providing a default value for the query parameter.

```python
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(min_length = 3)]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

#### Query parameter list / multiple values

When you define a query parameter explicitly with `Query`, you can make it accept a list of values (i.e., multiple values). In this case, the client can use the query parameter multiple times as in http://localhost:5000/items/?q=foo&q=bar, declare the query parameter as a `list[str]`:

```python
@app.get("/items/")
async def read_items(q: Annotated[list[str], Query()]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

and `q` will be a list of strings.

| NOTE: |
| :---- |
| To declare a query parameter with a type of `list` you need to explicitly use `Query`. Otherwise, the parameter would be interpreted as a request body. |

The interactive docs will be updated accordingly to allow sending an array of strings for `q`.

You can also provide default values for the list:


```python
@app.get("/items/")
async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

| NOTE: |
| :---- |
| You can also use `list` instead of `list[str]`. In those cases, FastAPI won't check the contents of the list. |

#### Declaring additional metadata

You can add more inforamtion about the parameter via `Query` . That information will be included in the generated OpenAPI spec.

You can add a `title` for the parameter:


```python
@app.get("/items/")
async def read_items(
    q: Annotated[str | None,
    Query(title="Query string", min_length=3)] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

You can add a `description` for the parameter:

```python
@app.get("/items/")
async def read_items(
    q: Annotated[str | None,
    Query(
        title="Query string",
        description="Query string for the items to search in the db",
        min_length=3,
    )] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

#### Alias parameters

In certain situations you will need a parameter in the HTTP request to have a name that won't be a valid Python variable name:

```
http://localhost:5000/items/?item-query=foobar
```

In those cases, you can use the `alias` parameter in `Query`:

```python
@app.get("/items/")
async def read_items(
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

#### Deprecating parameters

To document an existing parameter as deprecated, you can use  `deprecated=True` in the `Query`:

```python
@app.get("/items/")
async def read_items(
    q: Annotated[str | None,
    Query(
        alias="item-query",
        min_length=3,
        deprecated=True,
    )] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

That information will be transferred to the OpenAPI spec.

#### Excluding parameters from OpenAPI

To exclude a query parameter from the generated OpenAPI schema, set `include_in_schema=False` in `Query`:

```python
@app.get("/items/")
async def read_items(
    hidden_query: Annotated[str | None,
    Query(include_in_schema=False)] = None,
):
    if hidden_query:
        results.update({"hidden_query": hidden_query})
    else:
        return {"hidden_query": "Not found"}
    return results
```

#### Custom Validation

In some cases, you may need to do some custom validation that is not performed by FastAPI itself.

In those cases, you can use a custom validator function, which will be applied after the normal validation performed by FastAPI (e.g., after checking the value provided is a str of certain length).

This can be done using Pydantic's `AfterValidator` inside `Annotated`.

In the example below, the custom validator checks that the item ID starts with "isbn-" for books or "imdb-" for movies.

```python
import random
from typing import Annotated

from fastapi import FastAPI
from pydantic import AfterValidator

app = FastAPI()

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError("Invalid ID format. It must start with 'isbn-' or 'imdb-'")
    return id

@app.get("/items/")
async def read_items(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}
```

| NOTE: |
| :---- |
| Note that `AfterValidator` do not require using `Query`, but both can be used together. |

### Path parameters and numeric validations

In the same way you can declare validations and metadata for query parameters, you can follow the same approach for path parameters with `Annotated` and `Path`:

```python
@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

The snippet above declares an annotated `item_id` path parameter, with an additional title metadata.

| NOTE: |
| :---- |
| A path parameter is always required. |

#### Number validations

With `Query` and `Path` (among others) you can declare number constraints:

```python
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)], q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
```

The snippet above includes validates that `item_id >= 1`.

The numeric validations you can use are:
+ `gt`
+ `ge`
+ `le`
+ `lt`

This validations work for both ints and floats.

If any of these validations fail, FastAPI will automatically return an HTTP 422.

### Query Parameter Models

You can create a Pydantic model to declare a group of query parameters that are related.

While it may seem as an overkill, this approach would allow you to reuse the model in multiple places and also declare validations and metadata once.

```python
from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
```

The snippet above define a `FilterParams` model for the pagination, search, and sorting functionality of your APIs. Then, in the path operation, you use the `Query()` class to let FastAPI know the fields in FilterParams model are query parameters.

#### Forbidding extra query parameters when using Pydantic Models

When using Pydantic model configuration, you can prevent the client from sending extra query parameters using:

```python
class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []
```

If the client tries to send some extra query paremeters, they will receive an error response 422 (Unprocessable Content).

### Body: Multiple parameters

You can mix `Path`, `Query`, and body parameters and FastAPI will know what to do.

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="Item ID", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results
```

Note that in the example above, the request body is optional.

#### Multiple body parameters

FastAPI lets you declare multiple body parameters (e.g., item and user):

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
):
    results = {"item_id": item_id, "item": item, "user": user}
```

When declaring multiple body parameters, FastAPI will use the parameter names as keys in the body, so that the body should look like:

```json
{
    "item": {
        "name": "Foo",
        "description": "Bar",
        "price": 123.45,
        "tax": 6.78
    },
    "user": {
        "username": "jason",
        "full_name": "Jason Isaacs"
    }
}
```

#### Singular values in body

FastAPI provides a `Body()` class similar to `Query` and `Path`.

A scenario in which `Body()` comes in handy is when you want to add a singular parameter to the request body (not defined in the corresponding Pydantic models).

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body()],
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
```

Note that by default, a singular parameter will be identified as a query parameter by FastAPI. By using `Body()`, you let FastAPI know that `importance` is a request body parameter.

In this case, FastAPI will expect the following:

```json
{
    "item": {
        "name": "Foo",
        "description": "Bar",
        "price": 123.45,
        "tax": 6.78
    },
    "user": {
        "username": "jason",
        "full_name": "Jason Isaacs"
    },
    "importance": 5
}
```

#### Multiple body and query parameters

You can declare additional query parameters when declaring multiple body parameters (and there's no need to use `Query` if those are singular values):

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body()],
    q: str | None = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results
```

#### Embeddding body parameters

In certain scenarios, you might need to receive a request body such as:

```json
{
    "item": {
        "name": "Foo",
        "description": "Bar",
        "price": 42.0,
        "tax": 3.2
    }
}
```

instead of:

```json
{
    "name": "Foo",
    "description": "Bar",
    "price": 42.0,
    "tax": 3.2
}
```

This just requires using `Body(embed=True)` in your body parameter declaration:

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[Item, Body(embed=True)],
):
    results = {"item_id": item_id, "item": item}
    return results
```

### Body: fields

Validation and metadata for request body parameters is declared using `pydantic.Field`:

```python
from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Annotated[str | None, Field(
        title="Description of the item",
        max_length=3,
    )] = None
    price: Annotated[float, Field(
        gt=0, description="Price of the item (must be greater than zero)",
    )]
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
```

### Body: nested models

FastAPI supports arbitrarily nested models in your request body parameters.

#### List fields

You can define an attribute to be a subtype, such as `list`:

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list = []

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
```

Note that in the snippet above, the list doesn't declare the type of the elements.

Declaring a list with a type parameter is also supported:

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
```

#### Set fields

Similarly, you can use sets:

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
```

Note that when using sets, if you receive a request with duplicated data it will be automatically converted to a set of unique items. The corresponding documentation will be also updated to reflect that fact.

#### Nested models

The attribute type of a Pydantic model can itself be another Pydantic model. This leads to deeply nested model objects with specific attribute names, types, and validations as seen below:

```python
class Image(BaseModel):
    url: str
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

The payload your path operation expects will look like the following:

```json
{
    "name": "Foo",
    "description": "Bar",
    "price": 12.34,
    "tax": 56.78,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/foobar.png",
        "name": "foobar's image"
    }
}
```

#### Special types and validation

FastAPI allows you to use the special types Pydantic support such as `HttpUrl`.

For example, the previous example could have been written as:


```python
from pydantic import BaseModel, HttpUrl
...

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

When doing so, the string will be checked to be a valid URL, and documented in the corresponding JSON schema of the OpenAPI spec document.

#### Attributes with a list of submodels

You can use Pydantic models as the type elements for  list, set, etc.:

```python
from pydantic import BaseModel, HttpUrl
...

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
```

This will accept the following JSON body:

```json
{
    "name": "Foo",
    "description": "Bar",
    "price": 12.34,
    "tax": 56.78,
    "tags": ["rock", "metal", "bar"],
    "image": [
        {
            "url": "http://example.com/foobar.png",
            "name": "foobar's image"
        },
        {
            "url": "http://example.com/baz.png",
            "name": "baz image"
        }
    ]
}
```

#### Deeply nested models

You can define arbitrarily deeply nested models:

```python
class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None

class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]

@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer
```

#### Bodies of pure lists

If you expect as payload a JSON array at the top level, you can declare the type in the parameter of the function, instead of in the corresponding Pydantic model:

```python
class Image(BaseModel):
    url: HttpUrl
    name: str

@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images
```

This will accept a payload such as:

```json
[
    {
        "url": "http://example.com/foobar.png",
        "name": "foobar's image"
    },
    {
        "url": "http://example.com/baz.png",
        "name": "baz image"
    }
]
```

where the top-level JSON item is an array and not an object.

#### Bodies of arbitrary dicts

You can declare your body parameter as a dict (i.e., a dict instead of a Pydantic model).

That might come useful if you don't know beforehand the field names of the request that you will need to manage:

```python
@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights
```

Please note that JSON only supports string keys, but FastAPI will handle the conversion and validation as required.

### Declaring Request Example Data

You can declare examples for Pydantic models. Those will be added to the generated JSON schema as documentation:

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice item",
                    "price": 35.4,
                    "tax": 3.2
                }
            ]
        }
    }
```

#### `Field` examples

You can add examples when declaring fields:

```python
class Item(BaseModel):
    name: str
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float
    tax: float | None = None
```

You can use the same approach with:
+ `Path()`
+ `Query()`
+ `Header()`
+ `Cookie()`
+ `Body()`
+ `Form()`
+ `File()`

#### `Body` examples

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2
                },
            ],
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results
```

You can also pass multiple examples:

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2
                },
                {
                    "name": "Bar",
                    "price": 35.4,
                },
                {
                    "name": "Baz",
                    "price": 35.4,
                    "tax": 3.2
                },
            ],
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results
```

#### OpenAPI-specific examples

Before JSON Schema supported examples, OpenAPI supported them. You can declare this OpenAPI-specific examples in FastAPI with the `openapi_examples` argument, suppported in:
+ `Path()`
+ `Query()`
+ `Header()`
+ `Cookie()`
+ `Body()`
+ `Form()`
+ `File()`

Each specific example `dict` can contain:
+ `summary`: short description for the example.
+ `description`: long description that can contain Markdown text.
+ `value`: the actual example.
+ `externalValue`: an alternative to `value`, which is a URL pointing to the example.

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2
                    }
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `float`s.",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    }
                },
            },
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results
```

### Extra data types you can use in FastAPI

Apart from the common data types, the following additional data types you can use in FastAPI with the same level of functionalities you'll get for `int`, `float` or `str`:

+ `UUID`: in requests and responses, it will be represented as `str`.
+ `datetime.datetime`: in requests and responses, it will be represented as a `str` in ISO8601 format ("2026-02-13-T08:28:00+02:00").
+ `datetime.date`: in requests and responses, it will be represented as a `str` in ISO8601 format ("2026-02-13").
+ `datetime.time`: in requests and responses, it will be represented as a `str` in ISO8601 format ("08:33:24.045").
+ `datetime.timedelta`: in requests and responses, it will be represented as a `float` representing a value in seconds. Pydantic also allows representing it in ISO8601 format.
+ `bytes`: in requests and responses, it will be represented as `str`. The generated schema will specify it's a string with binary format.
+ `Decimal`: in requests and responses, it will be represeted as a `float`.

The following is an example illustrating some of these types:

```python
from datetime import datetime, time, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }
```

### Cookie Parameters

Cookie parameters are defined with `Cookie()` in the same way you define query and path parameters with `Query()` and `Path()`.

```python
@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}
```

| NOTE: |
| :---- |
| HTTP clients send cookies to the server as regular HTTP headers. |

#### Cookie parameter models

If you have a group of cookies that are related, you can create a Pydantic model to declare them.

This would allow you to reuse the model in multiple places and declare validations and metadata in a central place (using the same technique you can use for `Query`, and that can be applied to `Header()` as well).

```python
class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies
```

#### Forbidding extra cookies

In some cases, you might need to restrict the cookies that you want to receive.

```python
class Cookies(BaseModel):
    model_config = {"extra": "forbid"}

    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies
```

If a client tries to send extra cookies, they will receive an error response with code 422 (Unprocessable Content).


### Header Parameters

Header parameters are defined in the same way as query, path, and cookie parameters.

```python
from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
```

`Header()` has a little extra functionality on top of what `Path`, `Query`, and `Cookie` provide.

Standard HTTP headers are separated by a hypen as in `User-Agent`, but that variable name is not valid in Python.

By default, `Header()` will convert parameter names from `_` to hyphen to make them match what will be sent in the request.

Also, HTTP headers are case-insensitive, so you can declare them using Python's *snake_case* approach.

| NOTE: |
| :---- |
| If you need to disable automatic conversion of underscores to hyphens, you can use `Header(convert_underscores=False)`. |

#### Duplicate headers management

It is possible to receive duplicate headers. That is, you can receive the same header multiple times with multiple values.

In those cases, you can use a list in the type declaration:

```python
@app.get("/items/")
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}
```

#### Header parameter models

If you have a group of related header parameters, you can create a Pydantic model to declare them.

This allows you to reuse the model in multiple places and declared validations and metadata in a central place.

```python
class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers
```

#### Forbidding extra headers

In some cases, you might want to restrict the headers that you want to receive. You can do that using `model_config` as seen below:

```python
class CommonHeaders(BaseModel):
    model_config = {"extra": "forbid"}

    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers
```

If the client tries to send some extra headers, they will receive an 422 (Unprocessable Content) error response.

#### Disabling underscore conversions in header models

You can disable the conversion from "-" in the request to "_" in your path operation using:

```python
class CommonHeaders(BaseModel):
    model_config = {"extra": "forbid"}

    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header(convert_underscores=False)]):
    return headers
```

### Response model: return type

You can declare the type used for the response by annotating the path operation function return type:

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item

@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="foo", price=1.23),
        Item(name="bar", description="baz", price=3.21, tax=1.11)
    ]
```

FastAPI will use the return type to:
+ Validate the returned data: if the data you're returning does not match the expectations, it will return a server error 500 (Internal Server Error). This ensures your client receives the data shape they expect.
+ Add a JSON Schema for the response, in the OpenAPI path operation.

#### The `response_model` Parameter

There are scenarios where you may need to return some data that is not exactly what the type declares.

If you add the return type annotation, tools and editors will complain if you are returning a type (e.g., a `dict`) that is different from the declared returning type (i.e., the type hint for the return type is not a `dict` but a Pydantic model).

In those cases, you can use the `response_model` parameter in the path operation decorator instead of the return type:

```python
from typing import Any
...

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item

@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "foo", "price": 1.23},
        {"name": "bar", "description": "baz", "price": 3.21, "tax": 1.11}
    ]
```

FastAPI will use this `response_model` to do all the data documentation, validation, etc. and also to convert and filter the output data to its type declaration.

If you declare both a return type and a `response_model`, the `response_model` will take priority and that will be used by FastAPI.

| NOTE: |
| :---- |
| You can set `response_model=None` to disable creating a response model for a path operation. That might come in handy if you are adding type annotations for things that are not valid Pydantic fields. |

#### Using the same model as the request and response model

Consider the following snippet:

```python
from pydantic import BaseModel, EmailStr

class UserIn(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

@app.post("/user/")
async def create_user(user: UserIn) -> UserIn:
    return user
```

| NOTE: |
| :---- |
| To use `EmailStr` you will need to install [email-validator](https://github.com/JoshData/python-email-validator). |

In the example above, we are using the same model to declare both our input and output model for our request and response.

#### Using different models for request and response

FastAPI allows you to define different models for the request model (input model) and the response model (output model):

```python
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

@app.post("/user/")
async def create_user(user: UserIn, response_model=UserOut) -> Any:
    return user
```

Note that in this case, we can't annotate the path operation as:

```python
async def create_user(user: UserIn) -> UserOut:
```

because we are returning a `UserIn` instance and our tools and IDEs would complain about it.

#### Return Type and Data Filtering

If you just want to response model to filter some of the data available in the input model you can use inheritance:

```python
class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(BaseUser):
    password: str

@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user
```

Using this technique, you will get full editor and typecheck support for your response models.

#### Other return type annotations

There are scenarios where you need to return something that is not a valid Pydantic field and you annotate it (i.e., use type hints) in the function/coroutine, only to get the support provided by tooling.

The most common case would be returning a response directly.

```python
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, DirectResponse

app = FastAPI()

@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your portal"})
```

You can also use a subclass of `Response` in your type annotations:

```python
@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
```

#### Invalid return type annotations

However, if you return some other arbitrary object that is not a valid Pydantic type (e.g., a database object) and you annotate it like that in the function, FastAPI will try to create a Pydantic response model from that type annotation, and will fail.

The same would happen if you define the return type as the union of different types where one or more of them are not valid Pydantic types:

```python
# This fails
@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your portal"}
```

This fails because the type annotation is not a Pydantic type, and is not just a single `Response` class or subclass &mdash; it's a union between a `Response` and a `dict`.

In those cases, you might want to keep the type annotation to get support from tools and editors, while disabling the default data validations, documentation, filtering, etc. performed by FastAPI.

You can do that with `response_model=None`:

```python
@app.get("/portal", response_model=None)
async def get_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your portal"}
```

#### Response model: excluding default values

Consider the following snippet in which you have response model with default values:

```python
class Item(BaseModel):
    name: str
    desscription: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]
```

Setting `response_model_exclude_unset=True` comes in handy when you have models with many optional attributes (e.g., objects in a NoSQL database) and you don't want to send a very long JSON response full of default values.

For example, making a request to `GET /items/foo` will return:

```json
{
    "name": "Foo",
    "price": 50.2
}
```

Note that if your data has values for the model's fields with default values they will be included in the response.

Pydantic is smart enough to identify whether the values were set explicitly (instead of taken from the values) even if they have the same values as the defaults and will include them.

#### `response_model_include` and `response_model_exclude`

When you have to include or exclude a set of attributes from your model (provided that you have a single model in the response), you can use the `response_model_include` and `response_model_exclude` in the path operation decorator:

```python
class Item(BaseModel):
    name: str
    desscription: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}

@app.get("/items/{item_id}/name", response_model=Item, response_model_include={"name", "description"})
async def read_item_name(item_id: str):
    return items[item_id]

@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_name(item_id: str):
    return items[item_id]
```

Note however, that it is still recommended to use a hierarchy of model classes instead of these parameters, because the JSON Schema generated will be more faithful to what you are returning in your path operations.

### Extra models

It's relatively common to have more than one related models. For example, you might have a scenario involving a `User` model where:
+ the input model needs to have a password field.
+ the output model should exclude the password field.
+ the db model for the user needs a hashed password.

This can be done with multiple separate models:

```python
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved!")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
```

Note that Pydantic models have a `model_dump()` method that returns a dict with the model's data. Therefore, `UserInDB(**user_in.model_dump())` will convert `user_in` into a dict like the following:

```python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

and then `**` will pass the keys and values as arguments to `UserInDB`, so that you will end up with something like:

```python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

While this approach works, there's a lot of code duplication in the models.

The recommended approach is to rely on inheritance by creating a `UserBase` base class with the data that is common in the models and then specific subclasses to describe the `UserIn`, `UserOut`, and `UserInDB`:

```python
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    ...


class UserInDB(UserBase):
    hashed_password: str

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved!")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
```

#### Declaring a response to be the union of two or more types

You can declare a response to the the union of two or more types to indicate that the response would be any of them. This will be translated in the OpenAPI schema as `anyOf` of the corresponding JSON Schema models:

```python
class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type: str = "car"

class PlaneItem(BaseItem):
    type: str = "plane"
    size: int

items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]
```

Note that when using `response_model` instead of type annotations we have to use `Union` instead of `|`.

#### Declaring a response to be a list of objects

In the same way, you can declare responses to be a list of objects:


```python
class Item(BaseModel):
    name: str
    description: str


items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]

@app.get("/items/", response_model=list[Item])
async def read_items():
    return items
```

#### Declaring a response to be an arbitrary dict

You can also declare a response using a plain arbitrary dict. This is useful when you don't know the exact field names that would be required to define a Pydantic model beforehand:

```python
@app.get("/keyword-weights/", responde_model=dict[str, float])
async def read_keyword_heights():
    return {"foo": 2.3, "bar": 3.4}
```

### Response status code

You can declare the HTTP status code that should be used for the response of your path operation using the `status_code` parameter within your path operation decorator:

```python
@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}
```

You can also set `status_code` to an `IntEnum`, such as `http.HTTPStatus`, which features names to represent the status codes:

```python
from http import HTTPStatus

@app.post("/items/", status_code=HTTPStatus.OK)
async def create_item(name: str):
    return {"name": name}
```

or `fastapi.status`:

```python
from FastAPI import FastAPI, status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
```

#### HTTP status codes

Remember that:

+ 100-199: used for information. Responses with these status cannot have a body.
+ 200-299: used to indicate a successful response.
    + 200: "OK".
    + 201: "Created".
    + 204: "No Content". Used when there is no content to return to the client. The response must not have a body.
+ 300-399: used to indicate a redirection. Responses with these status may or may not have a body.
    + 304: "Not Modified". Must not have a body.
+ 400-499: used to indicate "Client error" responses.
    + 400: Generic error from the client.
    + 404: "Not Found".
+ 500-599: used to indicate "Server Error" responses.

### Form data

You can use `Form()` when you need to receive form fields instead of JSON.

| NOTE: |
| :---- |
| To use forms, you must first install [python-multipart](https://github.com/Kludex/python-multipart). |

```python
from type import Annotated

from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}
```

The way HTML forms (`<form></form>`) sends the data to the server uses a special encoding. Servers are notified of this particular encoding using the media type `application/x-www-form-urlencoded`. There is a variant of forms that include files, and that scenario is identified with the `multipart/form-data` media type.

#### Form models

You can use Pydantic models to declare form fields in FastAPI:

```python
from typing import Annotated

from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

class FormData(BaseModel):
    username: str
    password: str

@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data
```

If you review the docs, you will see that the request body is set to `application/x-www-form-urlencoded` and the fields will be available for you to test the path operation.

#### Forbidding extra form fields

As with Query, Cookie, Header, and Body, you can restric the form fields to only those declared in the Pydantic model using `model_config={"extra": "forbid"}`.

```python
from typing import Annotated

from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

class FormData(BaseModel):
    username: str
    password: str

    model_config = {"extra": "forbid"}

@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data
```

If the client tries to send an extra form field, it will receive a 422 (Unprocessable Content) error, and a body describing the error.

