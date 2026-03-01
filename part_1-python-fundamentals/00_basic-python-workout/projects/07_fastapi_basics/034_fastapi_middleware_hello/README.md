# 034: Hello, FastAPI middleware
> Illustrates the basics of FastAPI's middleware system
## Project description

FastAPI provides support for middlewares with both a decorator `@app.middleware("http")` and regular registration function `app.add_middleware()`.

Middlewares are functions/coroutines that are activated before the request is handed over to the path operation in charge so that the middleware can take over, and then activated again when the path operation is done, but response has not been sent back to the client.

These middlewares are activated in a predefined fashion, with the latest registered middleware added as the outermost, and the first ones as the innermost so if you have:

```python
app.add_middleware(middlewareA)
app.add_middleware(middlewareB)
```

The following activation will occur:

```
request ->
  MiddlewareB ->
    MiddlewareA ->
      path operation ->
    MiddleWareA ->
  Middleware B ->
response
```

### Creating a process time middleware

Create a middleware coroutine `add_process_time_header()` which adds a header `X-Process-Time` to the headers in the HTTP response with the time it took to execute the request.

In the case of multiple middlewares, should this middleware be the outermost or the innermost?

SOLUTION:

If you'd like to understand the whole time spent doing the request-response process, it should be the outermost, and therefore, defined the last one.

### Create a logging middleware

Create a middleware coroutine `add_http_logs()` coroutine which logs in the terminal the query parameters and body received.

Validate that once you have two middlewares, the expected activation lifecycle occurs.

SOLUTION:

Debugging you can see that the first middleware declared is the innermost and the second one is the outermost.

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
