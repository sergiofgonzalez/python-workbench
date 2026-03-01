# 042: Hello, FastAPI testing (when using /test dir)
> Illustrates the basics of FastAPI testing when using a /test dir

## Project description

ToDo

### TODO: illustrate what to do to develop some intuition on the concepts

ToDo

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
