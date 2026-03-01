# 037: Hello, FastAPI with multiple SQLModel models
> Illustrates how to use multiple SQLModel models with inheritance

## Project description

This project illustrates a slightly more advanced usage of [SQLModel](https://sqlmodel.tiangolo.com/) by building a very simple CRUD web app with FastAPI, backed by SQLite using a hierarchy of models to accommodate the different path operation needs.

The application features a single table.

### Create a CRUD API using a hierarchy of models for a `Hero` entity

1. Start by adding [`SQLModel`](https://sqlmodel.tiangolo.com/) to your dependencies.

1. Declare the connection string to your SQLite database file `database.db` by using the format: `sqlite:///database.db`.

1. Create the SQLModel engine (the object that holds the connections to the DB) by passing it the SQLite connection string and as args the dict `{"check_same_thread": False}` to allow FastAPI to use multithreading with the DB.

1. Declare a function `create_db_and_tables()` that does just that with `SQLModel.metadata.create_all()`.

1. Declare a dependency `get_session()` with a generator. In the implementation, you should use the `Session()` context manager and within the context you should simply yield the session.

1. Create a type annotation `SessionDep` for `get_session()`.

1. Register a function to be activated on FastAPI app startup by using the decorator `@app.on_event("startup")`. The function should be in charge of creating the DB and tables associated to the models.

1. Create the path operation for `POST /heroes/`.

    The path operation should receive a `HeroCreate` instance and return a `HeroPublic` instance. The former, needs to feature all the necessary fields to save a hero in the DB (`name`, optional `age`, `secret_name`), and the latter, the fields that can be shared with the client (`id`, `name`, and `age`). Design the class hierarchy supporting that.

1. Create the path operation for `GET /heroes/` supporting pagination with the `offset` and `limit` query parameters (the latter should be <= 100, with a default value of 100).

    The path operation should return a list of `HeroPublic` instances.

    In the path operation, use `session.exec().all()` to issue a SELECT of the hero instances. Note that you can directly send offset and limit to the SELECT.

1. Create a path operation for `GET /heroes/{hero_id}`. Use `session.get()` to retrieve an instance by its primary key. Return a 404 with detail "Hero not found", if the given id is not found in the DB.

    The path operation should return a `HeroPublic` instance.

1. Create a path operation for `PATCH /heroes/{hero_id}`. In the body, you must receive a `HeroUpdate` instance in which all fields subject of being updated should be declared as optional (i.e., all the fields but `id`).

    1. In the path operation, start by reading from the database the hero instance whose id matches the one given, returning a 404 with detail "Hero not found" when the instance is not found.

    1. Then, get a dictionary with the data sent in the body, where unset fields are excluded.

    1. Then use `SQLModel.sqlModel_update()` to update the DB instance with the data sent in the request.

    1. Commit, refresh the session object, and return a `HeroPublic` instance.

1. Create a path operation for `DELETE /heroes/{hero_id}`. Use `session.get()` to retrieve a hero instance by its primary key. Return a 404 with detail "Hero not found" if the given id is not found in the DB. Use `session.delete()` to remove the instance from the DB. Return a 204 No Content to indicate everything went OK.

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
