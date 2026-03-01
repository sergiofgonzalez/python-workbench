# 035: Hello, FastAPI CORSMiddleware
> Illustrates how to use FastAPI's CORSMiddleware

## Project description

You can use `CORSMiddleware` FastAPI's middleware whenever you need to allow a piece of JavaScript running in the browser to make cross-origin requests to your FastAPI backend.

This lab illustrates how you can use it.

### Using `CORSMiddleware`

Create a program that allows JavaScript running on http://localhost and http://localhost:8080 to make CORS (Cross-Origin Resource Sharing) to your backend.

Additionally, you should allow credentials, all methods, and all headers.

Note that to effectively test it, you'd need a frontend application with JavaScript sending HTTP requests.

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
