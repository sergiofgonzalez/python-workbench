# 036: Hello, SQLModel with FastAPI
> Illustrates the basics of SQLModel with a FastAPI app

## Project description

This project illustrates the basics of [SQLModel](https://sqlmodel.tiangolo.com/) by building a very simple web app with FastAPI, backed by SQLite.

### Create a CRUD API using a single `Hero` model

1. Start by adding [`SQLModel`](https://sqlmodel.tiangolo.com/) to your dependencies.

1. Declare your `Hero` model backed by a DB table featuring:
    + `id`: optional int, primary key of the table.
    + `name`: required str, indexed.
    + `age`: optional int, indexed.
    + `secret_name`: required str

1. Declare the connection string to your SQLite database file `database.db` by using the format: `sqlite:///database.db`.

1. Create the SQLModel engine (the object that holds the connections to the DB) by passing it the SQLite connection string and as args the dict `{"check_same_thread": False}` to allow FastAPI to use multithreading with the DB.

1. Declare a function `create_db_and_tables()` that does just that with `SQLModel.metadata.create_all()`.

1. Declare a dependency `get_session()` with a generator. In the implementation, you should use the `Session()` context manager and within the context you should simply yield the session.

1. Create a type annotation `SessionDep` for `get_session()`.

1. Register a function to be activated on FastAPI app startup by using the decorator `@app.on_event("startup")`. The function should be in charge of creating the DB and tables associated to the models.

1. Create the path operation for `POST /heroes/` to create heroes. You should receive a `Hero` instance, add it to the SQLModel's session, commit into the DB, and invoke refresh to update the hero in the session with the committed changes.

    Because we are using a single model, ensure that the client doesn't send the `id` field to prevent getting a unique constraint failure when trying to insert two records with the same `id`.

1. Create the path operation for `GET /heroes/` supporting pagination with the `offset` and `limit` query parameters (the latter should be <= 100, with a default value of 100).

    In the path operation, use `session.exec().all()` to issue a SELECT of the hero instances. Note that you can directly send offset and limit to the SELECT.

1. Create a path operation for `GET /heroes/{hero_id}`. Use `session.get()` to retrieve an instance by its primary key. Return a 404 with detail "Hero not found", if the given id is not found in the DB.

1. Create a path operation for `DELETE /heroes/{hero_id}`. Use `session.get()` to retrieve a hero instance by its primary key. Return a 404 with detail "Hero not found" if the given id is not found in the DB. Use `session.delete()` to remove the instance from the DB. Return a 204 No Content to indicate everything went OK.

1. Create  a path operation for `PUT /heroes/{hero_id}` that updates a full `Hero` instance. eturn a 404 with detail "Hero not found" if the given id is not found in the DB.


Test that:
+ `POST /heroes`
    - [X] Create a hero without sending an `id`.
    - [X] Create a hero sending an `id` should fail with 422.

+ `GET /heroes/`
    - [X] You get an empty list is returned when db is empty.
    - [X] Retrieves all heroes (one, several).
    - [X] Pagination limit works as expected.
    - [X] Pagination offset works as expected.
    - [X] Pagination limit and offset work as expected.

+ `GET /heroes/{hero_id}`
    - [X] You get a hero when you pass an existing id
    - [X] You get a 404 when you pass a non-existing id

+ `DELETE /heroes/{hero_id}`
    - [X] you delete a hero when passing an existing id
    - [X] you get a 404 when passing a non-existing id

+ `UPDATE /heroes/{hero_id}`
    - [X] you update a hero when passing an existing id an a full hero object in the bodywith no id
    - [X] you update a hero when passing an existing id an a full hero object with an id in the body that matches hero_id in path parameter
    - [X] it fails with 404 when passing a non-existing ID
    - [X] if fails with 422 with id in the path parameter and in the body do not match


Example payloads:

```bash
# Create a hero

$ http post :5000/heroes/ name="batman" age=33 secret_name="Bruce Wayne"
HTTP/1.1 200 OK
content-length: 61
content-type: application/json
date: Wed, 25 Feb 2026 07:51:06 GMT
server: uvicorn

{
    "age": 33,
    "id": 1,
    "name": "batman",
    "secret_name": "Bruce Wayne"
}
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
