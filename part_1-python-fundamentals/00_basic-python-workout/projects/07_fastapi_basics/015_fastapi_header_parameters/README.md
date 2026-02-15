# 015: Hello, FastAPI header parameters
> Illustrates the basics of FastAPI header parameters

## Project description

FastAPI lets you work with header parameters in the same way you manage query or path parameters.

You can also use Pydantic models for related headers.

### Defining header parameters

Create a path operation for `GET /items/` that accepts a header "User-Agent". Return the value of the header.

SOLUTION:

Because most of the tools send the User-Agent header, you don't need to use anything fancy:

```bash
$ http :5000/items/
```

### Duplicate header management

Create a path operation for `GET /v2/items/` that accepts an "X-Token" header that can appear multiple times. Return the values in that header.

SOLUTION:

This can be tested with:

```bash
$ http :5000/v2/items/ X-Token:1 X-Token:2
```

### Header parameter models

Create a Pydantic model `CommonHeaders` that groups related headers in a single model. It should feature the following fields:
+ host: required string
+ save_date: required boolean
+ if_modified_since: optional string, default value `None`.
+ traceparent: optional string, default value `None`.
+ x_tag: optional duplicate header with strings, default is empty list

Create a path operation for `GET /v3/items/` that accepts those `CommonHeaders`.

### Forbiding extra headers

Create a Pydantic model `CommonHeaders` that groups related headers in a single model. It should feature the following fields:
+ host: required string
+ save_date: required boolean
+ if_modified_since: optional string, default value `None`.
+ traceparent: optional string, default value `None`.
+ x_tag: optional duplicate header with strings, default is empty list

Create a path operation for `GET /items/` that accepts **only** those `CommonHeaders` (i.e., the request should fail if more headers are sent).

### Disabling underscore conversion

Create a path operation for `GET /v5/items/` that accepts an "X_Token" header. Use the `convert_underscores=False` to parse it.

SOLUTION:

You can test it with:

```bash
$ http :5000/v5/items/ x_token:1
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
