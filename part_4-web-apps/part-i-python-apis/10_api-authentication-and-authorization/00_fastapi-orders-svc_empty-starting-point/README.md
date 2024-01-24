# An Orders service using FastAPI
> empty starting point to add authentication and authorization to a FastAPI application.

## Description

This project implements a complete microservice for processing orders. It includes a web layer, a data access (repository) and a business layer.

The API implemented is documented in the [Orders OpenAPI spec](./oas.yaml), but Pydantic is used for the validation of the service endpoint payloads (both request and response).

This project represents an empty starting point (i.e., you need to go through the setup steps).

| NOTE: |
| :---- |
| All the commands below assume you're running outside of poetry's virtualenv and therefore `poetry run` is prefixing all the commands.<br>If you are in shell in which the virtualenv has been activated, you can run the command directly without the `poetry run` prepending it. |


### Setting up shop

The project is a copy of [03: FastAPI Orders service: prj layers](../../06_service-patterns/03-fastapi-orders-svc_prj_layers/) but has been migrated to Poetry.

As a result, to set up shop you need to do:

```bash
poetry install
```

This will create a virtual environment and install the required runtime and development dependencies.

| NOTE: |
| :---- |
| You can get all the details about the virtual environment (e.g., location) by running `poetry env info` . |


#### Alembic: One-time setup

[Alembic](https://alembic.sqlalchemy.org/en/latest/) is a lightweight db migration tool for usage with the SQL Alchema Database Toolkit for Python.

Before using it, you first need to do a one-time setup:

```bash
poetry run alembic init migrations
```

This will create a directory called `migrations/` with a configuration file `env.py` and a `migrations/versions/` directory. Additionally, you will find another configuration file in the root of the project `alembic.ini`.

The declaration for the `sqlalchemy.url` variable in the  `alembic.ini` file will have to be replaced with the name of the SQLite db file:

```ini
# file: alembic.ini
...

# sqlalchemy.url = driver://user:pass@localhost/dbname
sqlalchemy.url = sqlite:///orders.db
```

Finally, the `env.py` file will have to be modified to to look like:

```python
# file: migrations/env.py

...
# target_metadata = None
from orders.repository.models import Base
target_metadata = Base.metadata
```

This change enables Alembic to load our SQLAlchemy models and generate database tables from them, so that you don't need to create them yourself.

#### Alembic: Creating the initial migration

With the models of the data access layer already created, you can run the following command to prepare the creation of the initial schema:

```bash
poetry run alembic revision --autogenerate -m "Initial migration"
```

This creates a Python program with the necessary actions that have to be carried out in the database to create the schema. The file is To create the initial migration file under `migrations/versions`.

#### Alembic: Creating the schemas in the database

With the initial migration created type:

```bash
$ poetry run alembic upgrade heads
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 34f5d9b8abcb, Initial migration
```

This will create the `orders.db` file that will be used by SQLite to keep track of the data of our application. The database schemas derived from our models will have been created there as well.


#### Prism-cli: mock servers for Kitchen and Payments Services

You'll use `prism-cli` to start up mock servers for the Kitchen and Payments services. This will only require the OpenAPI spec.

```bash
npx @stoplight/prism-cli mock kitchen.yaml --port 3000
```

```bash
npx @stoplight/prism-cli mock payments.yaml --port 3001
```

#### Starting up the Orders Service

To run the project, type:

```bash
poetry run uvicorn orders.web.app:app --reload --port 8080
```

The endpoints can be tested from the Swagger UI which you can find at http://localhost:8080/docs/orders.


All the endpoints have been tested and worked mostly OK. There might be a few things that could be slightly improved such as the handling of the filters (i.e., they are sent to the business layer even if not specified as parameters in the query), or the field that is listed as an `int` in the model and should be a UUID string.

Nevertheless, the idea was to grasp how to create the layers of a relatively complex web app, and for that goal, it works 💯!

The project now also includes HTTPie.