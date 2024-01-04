# Implementing an Orders service using FastAPI
> Step 2: Introducing the DB Models (SQLAlchemy) and migrations (Alembic)

## Description

This project implements the DB models and migration strategy for the Orders service. The API implemented is documented in the [Orders OpenAPI spec](./oas.yaml), but it is not used for the validation of the service endpoint payloads.


### Setting up shop

The project uses venv for virtual environment management and pip for dependency management.

As a result, you just need to:

```bash
$ conda run -n web python -m venv .venv --upgrade-deps
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

#### Alembic: One-time setup

You should start by doing:

```python
alembic init migrations
```

This will create a directory called `migrations/` with a configuration file `env.py` and a `migrations/versions/` directory. Additionally, you will find another configuration file in the root of the project `alembic.ini`.

The declaration for the `sqlalchemy.url` variable will have to be replaced with the name of the SQLite db file:

```ini
# alembic.ini
...

# sqlalchemy.url = driver://user:pass@localhost/dbname
sqlalchemy.url = sqlite:///orders.db
```

Finally, the `env.py` file will have to be modified to to look like:

```python
# migrations/env.py

...
# target_metadata = None
from orders.repository.models import Base
target_metadata = Base.metadata
```

This change enables Alembic to load our SQLAlchemy models and generate database tables from them, so that you don't need to create them yourself.

#### Alembic: Creating the initial migration

With the models already created, run:

```bash
alembic revision --autogenerate -m "Initial migration"
```

To create the initial migration file under `migrations/versions`. This creates a Python program with the actions that will be carried out in the database.

#### Alembic: Creating the schemas in the database

With the initial migration created type:

```bash
$ alembic upgrade heads
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 34f5d9b8abcb, Initial migration
```

This will create the `orders.db` file that will be used by SQLite to keep track of the data of our application. The database schemas derived from our models will have been created there as well.

To run the project, type:

```bash
uvicorn orders.web.app:app --reload --port 8080
```

The endpoints can be tested from the Swagger UI which you can find at http://localhost:8080/docs/orders.
