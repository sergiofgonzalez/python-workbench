# Dependency Injection

## What's a Dependency?

A *dependency* is specific information that you need at some in your program.

While the usual approach is to write code that gets it right when you need it brings certain undesirable consequences in testing, etc.

Dependency injection is passing any specific information that a function needs into the function. For example, you can pass a helper function which you then can call to get the specific data.

## FastAPI Dependencies

FastAPI uses dependency injection to allow you to define dependencies as arguments to your functions and they will be automatically called by FastAPI and pass the values they return.

For example, let's consider the case of checking user authentication and authorization for some endpoints.

A `user_dep` dependency could get the user's name and password from HTTP arguments, look them up in a database, and return the token that you need to use to track the user afterwards. When doing so, your web-handling function doesn't ever call this directly &mdash; it will be handled automatically by FastAPI at function call time.

We saw some parts of that when we used endpoints with path, query, body, or HTTP header parameters.

Additionally, FastAPI lets you write your own functions, which will behave much as the built-in ones do.

## Writing a Dependency

A FastAPI dependency is something that is executed. As a result, it needs to be of type `Callable` (and therefore, needs to be either a function or a class).

The following snippet illustrate a very simple dependency function:

```python
from fastapi import FastAPI, Depends

app = FastAPI()

def user_dep(name: str, password: str):
    return {"name": name, "valid": True}

@app.get("/user")
def get_user(user: dict = Depends(user_dep)) -> dict:
    return user
```


The `user_dep` is a dependency function. It acts like a FastAPI path function in the sense that it has access to path and query parameters, etc. but it doesn't have a path decorator above it &mdash; it's a helper.

Then, the path function declares the `user` parameter as:

```python
@app.get("/user")
def get_user(user: dict = Depends(user_dep)) -> dict:
  ...
```

That syntax states that it expects an argument called user and that will be gotten from the value returned by the `user_dep()` function.

## Dependency Scope

FastAPI allows you to define dependencies that span a single path function, a group of them, or the whole web application.

### Single Path

In your path function, include an argument defined as:

```python
def path_func(arg_name: type = Depends(dep_func))
```

or alternatively:

```python
def path_func(arg_name: dep_func = Depends())
```

If your dependency function just checks something and doesn't return any values, you can also define the dependency in your path decorator:

```python
@app.method(url, dependencies=[Depends(dep_func)])
```

The following snippet illustrates this with a stupid use case in which `GET /user/check` fails unless the query `name=jason` is received.

```python
def check_user_dep(name: str):
    if name.lower() != "jason":
        raise ValueError(
            "name expected to be 'jason'"
        )

@app.get("/user/check", dependencies=[Depends(check_user_dep)])
def check_user() -> bool:
    return True
```

### Multiple Paths

In large FastAPI applications, it is common to have more than one *router* object, so that the `app` object has multiple routers with different endpoints attached to them.

In those cases, you can define dependencies that applied to all functions under the router (but only for that router).

```python
from fastapi import FastAPI, Depends, APIRouter

router = APIRouter(..., dependencies=[Depends(depfunc)])
```

### Global

You can add dependencies to your top-level FastAPI application object, and those will be applied to all its path functions.

```python
from fastapi import FastAPI, Depends

def depfunc1():
  pass

def depfunc2():
  pass

app = FastAPI(dependencies=[Depends(depfunc1), Depends(depfunc2)])

@app.get("/")
def get_root():
  pass
```
