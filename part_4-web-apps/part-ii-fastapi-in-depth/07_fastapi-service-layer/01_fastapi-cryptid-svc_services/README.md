# Cryptid service using FastAPI framework
> Step 4: implementing the service layer as a pass-through

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

## Testing the application

The implementation at this stage is a little bit all over the place as the web and data layer has not been adjusted.

There's a [unit test](tests/unit/service/test_creature.py) with the basic features.
