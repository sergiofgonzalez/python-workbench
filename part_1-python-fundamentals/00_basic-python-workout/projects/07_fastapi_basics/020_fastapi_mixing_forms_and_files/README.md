# 020: Mixing forms and files in FastAPI
> Illustrates how to mix forms and files in FastAPI

## Project description

FastAPI allows you to create programs that mix forms and files.

### Path operation with `Form()`, `File()`, and `UploadFile`.

Create a path operation for `POST /files/` in which you receive:
+ a required `File()` backed by `bytes`.
+ a required `UploadFile`
+ a token, which is a form field

In the implementation, return the file size of the bytes-backed field received, the `UploadFile`'s name and content type, and the token content.

SOLUTION:

This can be tested with:

```bash
$ http --form :5000/files/ file_a@main.py file_b@main.py token=token1
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
