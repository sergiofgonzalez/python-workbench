# FastAPI *hello, world!* app starting uvicorn internally

## Description

The simplest FastAPI app exposing a `GET /hi` endpoint that returns a hardcoded "Hello, world!" message.

In this project, `uvicorn` is started internally, so that you can start the web server doing:

```bash
$ poetry install

$ poetry run python hello/main.py --port 8080 --reload
```

