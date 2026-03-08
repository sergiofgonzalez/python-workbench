# 043: Hello, FastAPI SSE
> Illustrates the basics of FastAPI Server-Sent Events (SSE)

## Project description

SSE is a protocol that you can use to stream data to a client over HTTP.

When using it, you send *events*, pieces of text with fields, separated by blank lines such as:

```
data: {"name": "Portal Gun", "price": 999.99}

data: {"name": "Plumbus", "price": 32.99}
```

### Using SSE with Pydantic models

Create an application that streams to the client item models.

Start by creating a Pydantic model with the following shape:
+ name: required string
+ price: required float

Then, create a global set of items such as:

```python
items = [
    Item(name="Plumbus", price=32.99),
    Item(name="Portal Gun", price=999.99),
    Item(name="Meeseeks Box", price=49.99),
]
```

Then, create a `GET /items/stream` path operation that performs SSE streaming for those items.

Note that you will have to use `response_class=EventSourceResponse` in your path operation, and annotate your coroutine with `AsyncIterable[Item]`.

SOLUTION:

You can test it with a regular GET request from httpie.

### Using SSE with regular functions

Create an application that streams to the client item models.

Start by creating a Pydantic model with the following shape:
+ name: required string
+ price: required float

Then, create a global set of items such as:

```python
items = [
    Item(name="Plumbus", price=32.99),
    Item(name="Portal Gun", price=999.99),
    Item(name="Meeseeks Box", price=49.99),
]
```

Then, create a `GET /items/stream-no-async` path operation as a function that performs SSE streaming for those items.

Note that you will have to use `response_class=EventSourceResponse` in your path operation, and annotate your coroutine with `Iterable[Item]`.

SOLUTION:

You can test it with a regular GET request from httpie.

### Sending ServerSentEvent instances


Create an application that streams to the client item models.

Start by creating a Pydantic model with the following shape:
+ name: required string
+ price: required float

Then, create a global set of items such as:

```python
items = [
    Item(name="Plumbus", price=32.99),
    Item(name="Portal Gun", price=999.99),
    Item(name="Meeseeks Box", price=49.99),
]
```

Then, create a `GET /items/stream-events` path operation that performs SSE streaming for those items.

Note that you will have to use `response_class=EventSourceResponse` in your path operation, and annotate your coroutine with `AsyncIterable[ServerSentEvent]`.

Within the coroutine:
1. First yield a ServerSentEvent with the `comment`: "stream of item updates".
1. Then enumerate the items and return:
    + data=<the item>
    + event="item update"
    + id=i + 1
    + retry=5000

SOLUTION:

You can test it with a regular GET request from httpie.

```bash
$ http :5000/items/stream-events
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/event-stream; charset=utf-8
date: Sun, 08 Mar 2026 18:51:09 GMT
server: uvicorn
transfer-encoding: chunked
x-accel-buffering: no

: Starting stream of item updates

event: item update
data: {
    "name": "Item 1",
    "price": 10.0
}
id: 1
retry: 5000

event: item update
data: {
    "name": "Item 2",
    "price": 20.0
}
id: 2
retry: 5000

event: item update
data: {
    "name": "Item 3",
    "price": 30.0
}
id: 3
retry: 5000
```

### Sending raw data

Create an application that streams log lines to the client as raw data.

For that, create a `GET /items/stream-logs` path operation that performs SSE streaming for returning .

Note that you will have to use `response_class=EventSourceResponse` in your path operation, and annotate your coroutine with `AsyncIterable[ServerSentEvent]`:

```python
    logs = [
        "2025-01-01 INFO  Application started",
        "2025-01-01 DEBUG Connected to database",
        "2025-01-01 WARN  High memory usage detected",
    ]
```

as log events.

Within the coroutine, make sure you return `ServerSentEvent` instances with the log lines with `raw_data`.

SOLUTION:

You can test it from httpie with a regular GET request:

```bash
$ http :5000/items/stream-logs
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/event-stream; charset=utf-8
date: Sun, 08 Mar 2026 18:51:32 GMT
server: uvicorn
transfer-encoding: chunked
x-accel-buffering: no

data: 2024-06-01 12:00:00 INFO Starting server

data: 2024-06-01 12:01:00 INFO Received request for /items/stream

data: 2024-06-01 12:02:00 INFO Sent item updates to client
```

### Resuming with `Last-Event-ID`

Create a path operation for `GET /items/stream-resume` in which you receive a `Last-Event-ID` header with the value of the most recently processed event. Resume from that one.

Use the

```python
items = [
    Item(name="Plumbus", price=32.99),
    Item(name="Portal Gun", price=999.99),
    Item(name="Meeseeks Box", price=49.99),
]
```

SOLUTION:

You can test it with:

```bash
$ http :5000/items/stream-resume Last-Event-ID:2
```

### Implementing a POST path operation for SSE

Create a model for `Prompt` which holds some text.

Then, implement the path operation `POST /chat/stream` in which you return each of the words of the prompt you receive in the body as a `ServerSentEvent` where `data` is the word, and the `event` is `token`.

When finished send a `ServerSentEvent` where `raw_data="[DONE]"`, and `event` is done.

SOLUTION:

You can test it with:

```bash
$ http post :5000/chat/stream text="Hi, I am a useful assistant. How can I help you?"
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/event-stream; charset=utf-8
date: Sun, 08 Mar 2026 18:55:58 GMT
server: uvicorn
transfer-encoding: chunked
x-accel-buffering: no

event: token
data: "Hi,"

event: token
data: "I"

event: token
data: "am"

event: token
data: "a"

event: token
data: "useful"

event: token
data: "assistant."

event: token
data: "How"

event: token
data: "can"

event: token
data: "I"

event: token
data: "help"

event: token
data: "you?"

event: done
data: [DONE]
```

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
