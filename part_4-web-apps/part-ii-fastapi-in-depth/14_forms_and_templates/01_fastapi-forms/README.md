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

```bash
$ http --form GET localhost:8080/who name="Jason I
saacs"
HTTP/1.1 200 OK
content-length: 22
content-type: application/json
date: Fri, 08 Mar 2024 12:35:53 GMT
server: uvicorn

"Hello, Jason Isaacs!"
```