# FastAPI in depth: Building the Web Layer

A typical web application features three layers:

+ Web &mdash; where the API endpoints are defined. It typically handles the request processing concerns.

+ Service &mdash; where the business logic (i.e., the capabilities of the services) is defined.

+ Data &mdash; where data management capabilities and the interface to the persistent storage solution is defined.

Also, a typical web application will feature a few cross-layer components:

+ Model &mdash; data definitions, which might be relevant for different layers, such as request/response payload, model objects for the services, and database models that represents how objects are persisted).

+ Tests &mdash; unit, integration, and end-to-end tests.

This chapter will focus on the web layer.

| NOTE: |
| :---- |
| The web layer is sometimes called the API, Interface, or Router layer. |

The running example in the next few chapters revolves around an application involving management of *cryptids* (imaginary creatures) and the explorers who seek them.

## Strategies for designing a web app

When designing a web app, you can use the following strategies:

+ Start from the Web layer and work down &mdash; when you start from scratch and have analyzed the scope and requirements.

+ Data layer and work your way up &mdash; when you already have a database, and you're trying to make the data available to your consumers.

+ Service layer and work out in both directions &mdash; if you're following domain-drive design (DDD) and have clarity around the core entities and data models.

We will follow the *Start from the Web layer* approach.

## RESTful API Design concepts

The following table collects some basic concepts about REST:

| Concept | Definition |
| :------ | :--------- |
| Resources | Data elements your web app manages. |
| IDs | Unique resource identifiers. |
| URLs | Structured resource and ID strings. |
| Verbs (or actions) | Terms that accompany URLs for different purposes. |
| GET | Verb to retrieve a resource. |
| POST | Verb to create a new resource. |
| PUT | Verb to completely replace a resource. |
| PATCH | Verb to partially replace a resource. |
| DELETE | Verb to completely remove a resource. |

| NOTE: |
| :---- |
| While most authors recommend using plurals when naming resources (and related namespace such as API sections or db tables), sometimes using singular is simpler, mostly to accommodate the pluralization of English language. For example, we used `/orders` for the order service and it's OK, but if we are managing a child management web app, it would be `children/` and not `childs/`. |

## File and directory site layout

We can start from this:

```
00_prj_template/
├── README.md             # Project documentation
├── pyproject.toml        # Poetry
├── tests                 # Tests directory
│   └── __init__.py       # Treat dir as a package
└── webapp                # Source directory
    ├── __init__.py       # Treat dir as a package
    ├── data              # Data Layer
    ├── fake              # Fake/stub data
    ├── model             # Pydantic model definitions
    ├── service           # Business logic layer
    └── web               # Web layer
```

`__init__.py` files are files that are needed to identify the directory as a Python package (it's a sort of a Python convention). Most of the times those files are empty.

Python's import logic doesn't work strictly with directory hierarchies. It relies on Python *packages* and *modules*.

The `.py` files you create in the project directories are known as *Python modules*. Those contain the source code of your project. Their parent directories are packages if they contain an `__init__.py` file.

Python programs can import packages and modules. The Python interpreter has a built-in `sys.path` variable which includes the location of the standard Python library code.

```bash
$ poetry run python
>>> import sys
>>> sys.path
['', '/home/ubuntu/.pyenv/versions/3.10.13/lib/python310.zip', '/home/ubuntu/.pyenv/versions/3.10.13/lib/python3.10', '/home/ubuntu/.pyenv/versions/3.10.13/lib/python3.10/lib-dynload', '/home/ubuntu/.cache/pypoetry/virtualenvs/webapp-w1xYd7U8-py3.10/lib/python3.10/site-packages']
```

The environment variable `PYTHONPATH` is an empty or colon-separated string of directory names that tells Python which parent directories to check before `sys.path` is interrogated to import modules and packages.

For example, you could do:

```bash
export PYTHONPATH=$PWD/webapp
```

to ensure the packages in `/webapp` are considered before anything else.

## The main program

It is recommended to start from something like a [`main.py`](01_fastapi-cryptid-svc/cryptid/main.py).

```python
import os

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def top():
    return "root of the web layer here"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=os.getenv("PORT", 8080))
```

That simple structure lets you:
+ Start in *development mode* using `poetry run cryptid/main.py`. It will start the server in reload mode, using the default port 8080, which can be customized through an environment variable.

+ Start in *production mode* using `poetry run uvicorn cryptid.main:app --port 8080`.

## Testing the web app with HTTPie

```bash
http localhost:8000
```

## HTTP Requests

An HTTP request consist of a header followed by one or more body sections.

In a request you will also find path parameters (the values found in the URL as in `/echo/{msg}`, and query parameters (the infrmation found after the `?` in the URL as in `/greet/{who}?lang=en&mode=polite`).

HTTPie is a great tool to quickly check how HTTP requests look.

For example, the following command:

```bash
http -p HBh http://example.com
```

will print out:
- [X] 'H' request headers
- [X] 'B' request body
- [X] 'h' response headers
- [ ] 'b' response body
- [ ] 'm' response metadata

| NOTE: |
| :---- |
| You can review those details running `http --help`. |

## Multiple routers

While you can start with a single `app` variable in which you define all your endpoints, oftentimes your application will need to handle multiple kinds of resources.

In those cases, it's better to use multiple *subrouters*.

For example, in our application we will manage explorers and cryptids. We can create a *subrouter* for explorers, so that all endpoints related to the management of explorers are kept together in a separate file instead that in `main.py`.

```python
"""Explorer web layer in explorer.py"""
from fastapi import APIRouter

router = APIRouter(prefix="/explorer")


@router.get("/")
def top():
    return "root of explorer endpoint"
```

Then, in the `main.py` we do the linking:

```python
"""Entrypoint file: main.py"""
import os
from fastapi import FastAPI
from web import explorer

app = FastAPI()
app.include_router(explorer.router)


@app.get("/")
def top():
    return "root of the web layer here"
...
```

## Defining the data models

Let's define now the data that you'll be passing among layers.

This can be an iterative process, so let's set up the basis first which are the initial definitions for our Explorers and Creatures. Those can be added in separate files within the `model/` folder.

With the models defined, you can start creating stubs and fake data.

*Stubs* are canned results that are returned without calling the normal *"live"* modules. They're a quick way to test routes and responses.

*Fakes* are *stand-ins* for a real data source that performs some of the same functions. The most obvious example is an in-memory structure that mimics a database.

With so little analysis groundwork done at this point we don't have a lot of information about the access points, but we can assume we will need operations for:
+ Get one, some, all
+ Create
+ Replace completely
+ Modify partially
+ Delete

| NOTE: |
| :---- |
| Having completely isolates web, service, and data layers will let you scale your project very easily and ensure the expected degree of quality, as you'll be able to test the layers separately.<br>However, in certain projects, the service layer adds very little value. If that is the case you can skip the service layer, but keeping the web and data layer separate is a must. |

## Pagination and sorting

In the endpoints that return many or all things `GET /resource`, you will often want to implement:
+ sorting &mdash; order the results, even if you get only a set of them at a time
+ pagination &mdash; return only some resultt at a time, potentially respecting any sorting.

It's a common practice to provide that information as query parameters:

```
# sorting and pagination
GET /explorer?sort=country&offset=10&size=10

# sorting only
GET /explorer?sort=country&offset=10&size=10

# pagination only
GET /explorer?offset=10&size=10
```

It must be noted that sorting and pagination should occur in the data layer, and if possible on the database itself, as those system are prepared to handle those concerns very efficiently.
