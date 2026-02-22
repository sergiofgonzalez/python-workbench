# 021: Hello, HTTP error handling
> Illustrates the basics of HTTP error handling with FastAPI

## Project description

The following project illustrates several scenarios in which you can fine tune how you notify the client of an error.

These scenarios are intended to return HTTP status codes in the range 400-499 to signal there was an error from the client.

### Using FastAPI's `HTTPException`

Create a path operation for `GET /items/{item_id}` which raises an `HTTPException` when the item is not found within the `items` dictionary defined in your program. The path operation must return a 404 with the detail message "Item not found".

What error do you get if you don't raise the exception?

SOLUTION:
If you don't handle the exception yourself, instead of a 404 a 500 (Internal Server Error) will be sent.

### Adding custom headers to the error response

Create a path operation for `GET /v2/items/{item_id}` which raises an `HTTPException` when the item is not found within the `items` dictionary defined in your program. The path operation must return a 404 with the detail message "Item not found", and additionally, the header X-Error: "the item {item_id} was not found" must be sent.

### Registering a custom exception handler for a custom exception

Create an exception `MyCustomError` that can be instantiated by passing a `name`.

Then, register a custom exception handler for it by using the `@app.exception_handler()` decorator.

Then, in your path operation for `GET /v3/items/{item_id}` raise a `MyException()` when item_id features a particular value. Otherwise, return the received item_id and a message.

What happens if you don't register a custom exception handler?

SOLUTION:

If you don't implement your own custom handler, you'll get an HTTP 500.

### Overriding the default exception handlers: RequestValidationError

Register a custom handler for `RequestValidationError` exception. The handler should return a `PlainTextResponse` with the following contents:

```
Validation errors:
Field: {error['loc']}, Error: {error['msg']}
```

Then, in your path operation for `GET /v4/items/{item_id}` force a validation error by sending a string when you have declared `item_id` to be an int.

NOTE: the complete program will have multiple exception handlers registered, so you may need to comment/uncomment some of them.

### Overriding the default exception handlers: HTTPException

Register a custom handler for `HTTPException` exception. The handler should return a `PlainTextResponse` with the following contents:

```
HTTP error:
HTTP Exception: {str(exception)}
```

Then, in your path operation for `GET /v5/items/{item_id}` force an HTTPException whenever the `item_id` is equal to 3.

Test what happens when you don't follow the guidance given in the documentation that states:
+ In the custom handler, you should use Starlette's HTTPException
+ When raising the exception, you should use FastAPI's HTTPException

SOLUTION:

The application works well even when using fastapi.HTTPException in the event handler, however, we should be using the guidance from the docs.

### Using the `RequestValidationError` body in your custom handler

Register your own custom handler for `RequestValidationError` which should return the following an error message including the contents of the body, that is, a JSON response whose content is `{"detail": exc.errors(), "body": exc.body}`.

HINT: you might need to use `jsonable_encoder`.

In your path operation, accept an `Item` model featuring:
+ title: required str
+ size: required int

and call the operation sending a str for the size.

NOTE: at this point you will have multiple exception handlers registered, so you may need to comment/uncomment some of them.

SOLUTION:

You can test it with:

```bash
$ http post :5000/v6/items/ title="foo" size=xl
```

### Reusing FastAPI's exception handlers

Register custom exception handlers for HTTPException and RequestValidationError
which should print something on the screen and delegate the actual handling to FastAPIs own handlers.

Then, define a path operation you can use to check both errors (validation in the request and generic HTTPException).

NOTE: at this point you will have multiple exception handlers registered, so you may need to comment/uncomment some of them.

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
