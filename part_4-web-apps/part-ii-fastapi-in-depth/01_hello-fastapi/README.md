# Hello, FastAPI

## Hello, world!

The minimal FastAPI program looks like the following:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hi")
def greet():
  return "Hello, world!"
```

Those lines of code declare a simple `GET /hi` endpoint that responds with a greeting.

+ `app` is the top-level FastAPI object that represents the whole application.

+ `@app.get("/hi")` is a path decorator that declares the endpoint.

+ `greet()` is known as the *path function*.


To run this web application you need a web server and FastAPI doesn't package one. The recommendation is to use Uvicorn. Once installed, you can run the application doing:

```bash
uvicorn --port 8080 --reload
```

Alternatively, you can start uvicorn in your application:

```bash
from fastapi import FastAPI

app = FastAPI()


@app.get("/hi")
def greet():
    return "Hello, world!"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("hello.main:app", reload=True, port=8080)
```

The following pieces of code illustrates how to enable an endpoint with path and query parameters:

1. Path parameters:

    ```python
    @app.get("/hi/{who}")
    def greet(who):
        return f"Hello, {who}!"
    ```

2. Query parameters:

    ```python
    @app.get("/hi")
    def greet(who):
        return f"Hello, {who}!"
    ```

Handling information in the request body is also very simple:

```python
@app.post("/hi")
def greet(who: str = Body(embed=True)):
    return f"Hello, {who}!"
```

Note that we had to change the endpoint verb to a post, because FastAPI assumes that GET requests shouldn't have a body.

The `Body(embed=True)` is a way to tell FastAPI that who is coming from a JSON formatted request body with the `who` key embedded in the JSON (that is, we're expecting a `{"who": "your-name-here"}`).


In a similar way, handling header parameters is also very easy. FastAPI automatically maps hyphens to underscores, so that you can do:

```python
@app.get("/hi")
def greet(who: str = Header()):
    return f"Hello, {who}!"


@app.get("/agent")
def get_agent(user_agent: str = Header()):
    return f"User-Agent: {user_agent}"
```

## HTTP Responses

+ FastAPI converts everything you return from your endpoint function to JSON (and the response will have the `Content-Type: application/json`).

+ By default FastAPI returns a 200 status code an 4xx codes when an exception is found. You can fine tune the status code to return in the path decorator.

        ```python
        @app.get("/happy", status_code=202)
        def happy():
            return "😀"
        ```

+ You can easily inject HTTP headers in the response using:

        ```python
        @app.get("/header/{name}/{value}")
        def header(name: str, value: str, response: Response):
            response.headers[name] = value
            return f"header {name} has been injected!"
        ```

### Response types

We've established that the defaul in FastAPI is a JSON response. However, you can also return the following response types available in `fastapi.responses`:

+ `JSONResponse`
+ `HTMLResponse`
+ `PlainTextResponse`
+ `RedirectResponse`
+ `FileResponse`
+ `StreamingResponse`


You can use them as follows:

```python
...
from fastapi.responses import HTMLResponse, PlainTextResponse
...

@app.get("/plain", response_class=PlainTextResponse)
def plain_response():
    return "Hello!"


@app.get("/html", response_class=HTMLResponse)
def html_response():
    return """
        <!doctype html>
        <head>
            <title>Hello, html!</title>
        </head>
        <body>
            <h1>Hello, html!</h1>
        </body>
        </html>
        """

```

If that is not sufficient, you can use a generic `Response` class:

```python
@app.get("/xml")
def xml_response():
    data = """<?xml version="1.0"?>
    <person>
        <name>Jason</name>
        <surname>Isaacs</surname>
    </person>
    """
    return Response(content=data, media_type="application/xml")
```

### Type conversion

FastAPI converts any result you're returning from your function into a JSON using an internal function called `jsonable_encoder()`.

FastAPI uses that function to convert any data structure you're returning into a "JSONable" Python data structure that can be sent to `json.dumps()` and returns that string. The framework will also update the `Content-Length` and `Content-Type` http headers.

### Model Types and `response_model`

Consider the following contrived example in which you are creating an application that lets a user create and retrieve tags, which are nothing more than strings wrapped in a class.

It is only natural that you will need to define the following model variants:
+ a `Tag` class that represents the class in the database. Therefore, it will include fields such as ID and a created datetime.

+ a `TagIn` class that represents the information that the user must provide to create the tag. In our simplistic example, this will be just a string.

+ a `TagOut` class that represents the information that is returned from the database. In our example, that will be the string and the creation datetime, but not the ID.

FastAPI provides a `response_model` attribute in the path decorator that you can use to filter out the information you return.

That is, if you decorate a path with a `response_model=TagOut`, you can return a `Tag` instance in your path function, and let FastAPI convert the response automatically into an instance of `TagOut` removing the unwanted fields from the response.

The following snippet illustrates how to do it:

```python
import uuid
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class TagIn(BaseModel):
    tag: str


class Tag(BaseModel):
    id: str
    tag: str
    created: datetime


class TagOut(BaseModel):
    tag: str
    created: datetime


tags: dict[str, Tag] = dict()


@app.post("/", status_code=201)
def create(tag_in: TagIn) -> TagIn:
    tag: Tag = Tag(
        id=str(str(uuid.uuid4())), tag=tag_in.tag, created=datetime.utcnow()
    )
    tags[tag.tag] = tag
    return tag_in


@app.get("/{tag_str}", response_model=TagOut)
def get_one(tag_str: str) -> TagOut:
    if tag_str in tags:
        tag = tags[tag_str]
        return tag  # type: ignore
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Tag {tag_str!r} was not found",
        )
```

See how the `get_one()` path function uses `response_model=TagOut` and therefore, even when returning a `Tag` instance, the client will receive:

```
$ http localhost:8080/tagname
HTTP/1.1 200 OK

{
    "created": "2024-01-19T13:17:45.980876",
    "tag": "tagname"
}
```


| EXAMPLE: |
| :------- |
| See [10_tags-filter-response-model](10_tags-filter-response-model/README.md) for a runnable example. |