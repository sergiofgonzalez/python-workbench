# 014: Hello, FastAPI cookie parameters
> Illustrates the basics of FastAPI cookie parameters

## Project description

FastAPI lets you work with cookie parameters in the same way you manage query or path parameters.

You can also use Pydantic models for related cookies.

### Dealing with cookie parameters with `Cookie()`

Create a path operation for `GET /items/` in which you receive a cookie parameter `ads_id`. Return that parameter in the response.

SOLUTION:

This can be tested with

```bash
$ http get :5000/items/ Cookie:ads_id=1234
```

### Cookie parameter models

Create a Pydantic model `Cookies` with fields:
+ session_id: required string
+ app1_tracker: optional string, default value `None`
+ app2_tracker: optional string, default value `None`


Then create a path operation for `GET /v2/items/` which uses the cookies defined in the Pydantic model.

SOLUTION:

This can be tested with:

```bash
$ http get :5000/v2/items/ Cookie:"session_id=1;app1_tracker=2;app2_tracker=3"
```

### Forbiding extra cookies

Using Pydantic models, define a `Cookies` model with fields:
+ session_id: required string
+ app1_tracker: optional string, default value `None`
+ app2_tracker: optional string

And a path operation for `GET /v3/items/` which uses the cookies defined in the Pydantic model and that doesn't allow to add extra cookies.


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
