# 016: Hello, FastAPI response models
> Illustrates the basics of FastAPI response models

## Project description

In FastAPI, you can declare the type used for the response by annotating the path operation function return type. FastAPI will then take over and perform data conversion, validation, documentation, etc.

### Returning a model and a list of models

Create a FastAPI app that defines an `Item` model with the following fields:
+ name: required string
+ description: optional string
+ price: required float
+ tax: optional float
+ tags: optional list of strings, default value an empty list

Then create:
+ a path operation for `POST /items/` that returns the item received in the request body.
+ a path operation for `GET /items/` that returns a static list of items (e.g., `[Item(name="foo", price=1.23), Item(name="bar", description="baz", price=3.21, tax=1.11)]`).

Test the program making sure that FastAPI validates and converts the data as needed. What error do you get when the validation of the response fails? Review the /docs.

SOLUTION:

When the output validation fails you get an HTTP 500.

### Using `response_model` instead of return type annotations

You can use `response_model` to declare your return type instead of declaring your return type via type hints.

This is useful when you are returning something different from the specified type.

Familiarize yourself with this scenario by creating a FastAPI app that defines an `Item` model with the following fields:
+ name: required string
+ description: optional string
+ price: required float
+ tax: optional float
+ tags: optional list of strings, default value an empty list

Then create:
+ a `POST /v2/items/` that declares the response type of the coroutine as `Any` but uses `response_model` to declare the response type (an `Item`).
+ a `GET /v2/items/` that declares the response type of the coroutine as `Any` but uses `response_model` to declare the response type (a list of `Item`).

Test the program making sure that FastAPI validates and converts the data as needed. What error do you get when the validation of the response fails? Review the /docs.

### Using the same model in the request body and as the response model

Create model `UserIn` with the following fields:
+ username: required str
+ email: required EmailStr (you may need to install [email-validator](https://github.com/JoshData/python-email-validator) as a dependency).
+ full_name: optional str

Then define a path operation for `POST /user/` that receives and returns a `UserIn` object.

### Using different models for request and response

Create model `UserInV2` with the following fields:
+ username: required str
+ password: required str
+ email: required EmailStr (you may need to install [email-validator](https://github.com/JoshData/python-email-validator) as a dependency).
+ full_name: optional str

Then create another model `UserOut` which is identical to `UserIn` minus the password field.

Then define a path operation for `POST /v2/user/` that receives a `UserIn` and returns a `UserOut` object. Can you declare `UserOut` without doing any field manipulation? How can you fix it?

Create a solution for a path operation `POST /v3/user/` that allows you to use type hints using a hierarchy of models. This is known as data filtering.

SOLUTION:
1. Yes, you can declare `UserOut` using type hints and it works as if you had used `response_model`. However, the IDE/type tools will report that you're returning something different from the declared return type.

#### Using `Response` as the return type

When you want to return something that is not a Pydantic model and you want to use type hints you can use `Response` and their subclasses.

Create a path operation for `GET /portal` which optionally receives a query parameter `teleport`, whose default value is `False` and does the following:
+ if teleport is true, return a `RedirectResponse` to https://www.youtube.com/watch?v=dQw4w9WgXcQ.
+ otherwise, return a `JSONResponse` whose content is the dictionary `{"message": "Here's your portal"}`.

Declare the path operation return type as `Response`.


Create another path operation `GET /teleport` that directly returns a `RedirectResponse` to https://www.youtube.com/watch?v=dQw4w9WgXcQ and declares `RedirectResponse` as the response type.

Test it and review the /docs.

#### Invalid return types and `response_model=None`

Note that you cannot declare the return type as the union of different types where one or more of them are not valid Pydantic types.

Illustrate this fact by creating a path operation for `GET /portal2` where you declare a union of `Response` and `dict` as the return type and in the path operation return either a `Redirect` response (as in the previous `GET /portal` example) or the dict `{"message": "Here's your portal"}`. What is the error/exception you get?

Use `response_model=None` to fix it (this disable FastAPI's management of the response, that is, the validation, conversion, and documentation will be disabled).

SOLUTION:
You get a nasty exception:

```
fastapi.exceptions.FastAPIError: Invalid args for response field! Hint: check that starlette.responses.Response | dict[str, str] is a valid Pydantic field type. If you are using a return type annotation that is not a valid Pydantic field (e.g. Union[Response, dict, None]) you can disable generating the response model from the type annotation with the path operation decorator parameter response_model=None. Read more: https://fastapi.tiangolo.com/tutorial/response-model/
```


#### Excluding default values from the response

Create an `ItemV2` response model with the following fields:
+ name: required string
+ description: optional string
+ price: required float
+ tax: required float, with default value = 10.5
+ tags: optional list of strings, default value an empty list

Then declare the following dictionary of items:

```python
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}
```

Start by creating a `GET /items/{item_id}` path operation the returns the item received in the path. What is the behavior with the fields with default values?

Then create a `GET /v2/items/{item_id}` which uses `response_model_exclude_unset=True` and compare the results. What happens with the fields that are set but have the declared default values? Are they sent?

SOLUTION:
+ In `GET /items/{item_id}` you get all the fields returned no matter whether they have the default values or not.

    ```json
    // Foo
    {
        "description": null,
        "name": "Foo",
        "price": 50.2,
        "tags": [],
        "tax": null
    }

    // Baz
    {
        "description": null,
        "name": "Baz",
        "price": 50.2,
        "tags": [],
        "tax": 10.5
    }
    ```

+ In `GET /v2/items/{item_id}` you only get the fields that have been explicitly set:

    ```json
    // Foo
    {
        "name": "Foo",
        "price": 50.2
    }

    // Bar
    {
        "description": "The bartenders",
        "name": "Bar",
        "price": 62.0,
        "tax": 20.2
    }

    // Baz
    {
        "description": null,
        "name": "Baz",
        "price": 50.2,
        "tags": [],
        "tax": 10.5
    }
    ```

    Note also that the when an instance of the model explicitly sets a value, that is included in the response even if the value it sets is the default value.

### `response_model_include` and `response_model_exclude`

`response_model_include` and `response_model_exclude` can be used to include/exclude a specific set of fields from the response when you have a single response model.

Create an `Item` response model with the following fields:
+ name: required string
+ description: optional string
+ price: required float
+ tax: required float, with default value = 10.5
+ tags: optional list of strings, default value an empty list

Then declare the following dictionary of items:

```python
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
```

Start by creating a `GET /items/{item_id}/name` path operation the returns the item received in the path and uses `response_model_include` to include the name and description fields.

Then, create a `GET /items/{item_id}/public` path operation the returns the item received in the path and uses `response_model_exclude` to exclude the tax field from the response.

How would you do the same using model classes?

### Using separate models

It's common to use several Pydantic models when you deal with a scenario involving a user where:
+ the input model needs to have a password field.
+ the output model should exclude the password field.
+ the db model for the user needs a hashed password.

Create a `UserInV4` model with the fields:
+ username: required str
+ password: required str
+ email: required EmailStr
+ full_name: optional str

Create a `UserOutV4` model with the fields:
+ username: required str
+ email: required EmailStr
+ full_name: optional str

Create a `UserInDBV4` model with the fields:
+ username: required str
+ hashed_password: required str
+ email: required EmailStr
+ full_name: optional str

Then define a function `fake_password_hasher()` that receives a string and returns a *hashed* password consisting of prepending "supersecret" to the received string.

Then, define a function `fake_save_user()` that received a `UserIn` and hashes the password, creates a `UserInDB` instance and prints and returns the `UserInDB` instance.

Then create a path operation for `POST /v4/user/` that calls `fake_save_user()` and returns a `UserOut`.

Then, refactor the solution to use a model class hierarchy.

### Using Union with `response_model`

Create a model `BaseItem` featuring:
+ description: required str
+ type: required str

Create a model `CarItem` inheriting from `BaseItem` featuring:
+ type set to "car"

Create a model `PlaneItem` inheriting from `BaseItem` featuring:
+ type set to "plane"
+ size: required int

Then define the following items:

```python
items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}
```

Then, define a path operation for `GET /v3/items/{item_id}` which declares the `response_model` to be the union of `PlaneItem` or `CarItem` and returns the corresponding requested object.

Can the example be adjusted to use type hints instead?

SOLUTION:

Yes, you can use type hints instead.

### Declaring the response to be a list of objects:

Define a `ItemV3` model with fields:
+ description: required str
+ type: required str

Then define the following two items:

```python
items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]
```

Finally, define a path operation for `GET /v3/items/` that declares the `response_model` to be a list of items. Can this be done using type hints and obtain the same results?

### Declaring the response to be an arbitrary dict

Declare a path operation for `GET /keyword-weights/` which declares the response_model to be a dict whose keys are strings and values are float.

In your path operation return a compatible response. Can this be done with type hints instead? When would you use this approach instead of Pydantic models?

SOLUTION:

Yes, you can do pretty much everything with type hints.

You need to rely on responses with Python types such as `dict[str, float]` when you have responses with field names you can't predict. In the example above, you cannot predict the keywords you're going to find, and therefore, you cannot rely on a Pydantic model.


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
