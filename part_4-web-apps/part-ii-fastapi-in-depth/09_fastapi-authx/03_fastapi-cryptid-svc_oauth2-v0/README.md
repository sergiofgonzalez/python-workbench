# Cryptid service using FastAPI framework
> Step 8: adding (custom) OAuth2 authentication &mdash; v0.

This project illustrates how to build a web application that implements the management of *cryptids* (imaginary creatures) and the explorers who seek them.

This is the version 0 which follows the book recommendation, which features a couple of things I don't like that much:

+ The fake layer is used for both service and data layer. In my opinion, it should be created for the data layer only, otherwise, it makes the interface less consistent as the service and data function signatures are different.

+ The three resources (creatures, explorers, users) don't have a consistent interface for the CRUD, which complicates the testing and behavior.

+ The tests for the data layer cannot be executed individually &mdash; they depend on the sequential execution of the individual tests.

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

| NOTE: |
| :---- |
| The code of the data layer does not include `connection.commit()`. As a result, the database file is never updated, which helps with the testing.<br>If you want to persist the changes so that they survive server restarts you simply need to commit the changes after every operation that *changes* the database. |

## Testing the application

### Unit testing the data layer

A couple of PyTest files have been included in the `tests/unit/data/` directory. Those can be executed running:

```bash
pytest tests/unit/data/
```

In those tests, SQLite is configured to as an in-memory database, but there's some coupling between the individual tests.


### Manual Integration tests with HTTPie

#### Explorer

Sample HTTPie commands:

```bash
# Create explorer
$ http localhost:8080/explorer/ name="Beau Buffette" country="US" description="Manually created explorer"
```

```bash
# Replace entry (PUT)
$ http PUT localhost:8080/explorer/"Beau Buffette" name="Jason Isaacs" country="UK" description="Hello to Jason!"
```

```bash
# Partially modify entry (PATCH)
$ http patch localhost:8080/explorer/"Beau Buffette" name="Jason Isaacs"
```

```bash
# Delete entry
$ http delete http://localhost:8080/explorer/"Beau Buffette"
```


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

- [X] Try to define the same record twice should fail with 422.

    The server logs show: `ERROR:    cryptid.data.explorer : IntegrityError: cannot create explorer Beau Buffette: UNIQUE constraint failed: explorer.name`

- [X] Try to get a non-existent record should fail with 404

- [X] Replace the description of an explorer (using PUT)

- [X] Replace the name of an explorer with a new name (using PUT)

- [X] Replace the name of an explorer with one that already exists should fail with 422. (PUT)

- [X] Replace the name of an non-existent explorer should fail with 404 (PUT)

- [X] Replace the country of an explorer using PATCH

        ```bash
        $ http patch localhost:8080/explorer/"Beau Buffette" country="ES
        ```
- [X] Replace the country of non-existent explorer should fail with 404 (PATCH)

- [X] Replace the name of an explorer with one that already exists should fail with 422 (PATCH)

- [X] Replace the name of an explorer should work OK (PATCH)

- [X] Delete one that doesn't exist

- [X] Delete one that exists

#### Creature

Sample HTTPie commands:

```bash
# Create explorer
$ http localhost:8080/creature/ name="yeti" country="CN" area="Himalayas" description="Snowperson" aka="The Abominable Snowman"
```

```bash
# Replace entry (PUT)
$ http put localhost:8080/creature/yeti name="Sasquatch" country="CN" area="Himalayas" description="Snowperson" aka="yeti"
```

```bash
# Partially modify entry (PATCH)
$ http patch localhost:8080/creature/Yeti aka="Sasquatch"
```

```bash
# Delete entry
$ http delete localhost:8080/creature/Yeti
```


- [X] Get all creatures using `GET /creature/` should return an empty array.

- [X] Get all creatures using `GET /creature` should now work (with the two decorators).

- [X] Creature creation with mispelled property (e.g., `contry` should fail with 422).

- [X] Creture creation with correct attributes should work and return the created record (201 should be returned).

- [X] Now get all explorers should return the recently created record.

- [X] Get one should also work `GET /creaure/"yeti"`

- [X] Try to define the same record twice should fail with 422.

    The server logs show: `ERROR:    cryptid.data.creature : IntegrityError: cannot create creature yeti: UNIQUE constraint failed: creature.name`

- [X] Try to get a non-existent record should fail with 404

- [X] Replace the description of an creature (using PUT)

- [X] Replace the name of an creature with a new name (using PUT)

- [X] Replace the name of an creature with one that already exists should fail with 422. (PUT)

- [X] Replace the name of an non-existent creature should fail with 404 (PUT)

- [X] Replace the country of a creature using PATCH

- [X] Replace the country of non-existent creature should fail with 404 (PATCH)

- [X] Replace the name of an explorer with one that already exists should fail with 422 (PATCH)

- [X] Replace the name of an explorer should work OK (PATCH)

- [X] Delete one that doesn't exist

- [X] Delete one that exists