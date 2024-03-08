# FastAPI: serving static files

This project illustrates how to serve static files (like a traditional web server would do).

In `hellofile/public/` you will find an HTML/JS/CSS application that will be accessible on http://localhost:8080/public.


## Setting up shop

This project is configured with Poetry.

```bash
$ poetry install
```

Then you can either do:

This project is configured with Poetry.

```bash
$ poetry run uvicorn hellofile.main:app --port 8080 --reload
```

or simply:

```bash
poetry run python hellofile/main.py
```

## Testing the endpoint with HTTPie

Just visit http://localhost:8080/public