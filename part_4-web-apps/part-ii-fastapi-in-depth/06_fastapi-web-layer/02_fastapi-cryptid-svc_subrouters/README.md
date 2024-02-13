# Cryptid service using FastAPI framework
> Step 2: creating a subrouter and linking it to the app object

This project illustrates how to build a web application that implements the management of *cryptids* (imaginary creatures) and the explorers who seek them.

## Setting up shop

The project uses Poetry. To set things up type:

```bash
poetry install
```

## Running the application

To run the application in development mode type:

```bash
poetry run python cryptid/main.py
```

This will start the server in port 8080 with reloading enabled.

You can also run the application with `uvicorn`:

```bash
poetry run uvicorn cryptid.main:app \
  --port 8080 \
  --reload
```

## Testing the application with HTTPie

You can test the `/` and `/echo/{msg}` and `/explorer` endpoints with HTTPie:

```bash
$ http -b localhost:8080
"root of the web layer here"

$ http -b localhost:8080/echo/hello
"echo: hello"

# Note that `explorer` redirects to `explorer/`
$ http localhost:8080/explorer
HTTP/1.1 307 Temporary Redirect
content-length: 0
date: Wed, 07 Feb 2024 10:34:06 GMT
location: http://localhost:8080/explorer/
server: uvicorn

$ http -b localhost:8080/explorer/
"root of explorer endpoint"
```

