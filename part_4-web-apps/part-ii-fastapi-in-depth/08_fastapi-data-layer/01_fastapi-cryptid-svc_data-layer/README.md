# Cryptid service using FastAPI framework
> Step 6: implementing the data layer using SQLite and `sqlite3` module.

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

- [X] Get all explorers using `GET /explorer/` should return an empty array.

- [X] Get all explorers using `GET /explorer` should now work (with the two decorators).

- [X] Explorer creation with mispelled property (e.g., `contry` should fail with 422).

- [X] Explorer creation with correct attributes should work and return the created record (201 should be returned).

    ```bash
    $ http localhost:8080/explorer/ name="Beau Buffette" country="US" description="Manually created explorer"
    HTTP/1.1 200 OK
    content-length: 81
    content-type: application/json
    date: Mon, 12 Feb 2024 14:53:53 GMT
    server: uvicorn

    {
        "country": "US",
        "description": "Manually created explorer",
        "name": "Beau Buffette"
    }

    ```

- [X] Now get all explorers should return the recently created record.

- [X] Get one should also work `GET /explorer/"Beau Buffette"`

- [X] Try to define the same record twice should fail with 500.

    The server logs show: `sqlite3.IntegrityError: UNIQUE constraint failed: explorer.name`

- [X] Try to get a non-existent record should fail with 500

    The server logs show: `TypeError: cannot unpack non-iterable NoneType object`

In the next step we fix the previous errors before tackling the other methods within `/explorer` or the other resource (`/creature`).