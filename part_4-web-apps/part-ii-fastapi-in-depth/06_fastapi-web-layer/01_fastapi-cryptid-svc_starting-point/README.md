# Cryptid service using FastAPI framework
> Step 1: setting up the project structure and initial shakedown

This project illustrates how to build a web application that implements the management of *cryptids* (imaginary creatures) and the explorers who seek them.

## Setting up shop

The project uses Poetry. To set things up type:

```bash
poetry install
```

## Running the application

To run the application in development mode type:

```bash
poetry run cryptid/main.py
```

This will start the server in port 8080 with reloading enabled.

You can also run the application with `uvicorn`:

```bash
poetry run uvicorn cryptid.main:app \
  --port 8080 \
  --reload
```

## Testing the application with HTTPie

You can test the `/` and `/echo/{msg}` endpoints with HTTPie:

```bash
$ http -b localhost:8080
"root of the web layer here"

$ http -b localhost:8080/echo/hello
"echo: hello"
```

