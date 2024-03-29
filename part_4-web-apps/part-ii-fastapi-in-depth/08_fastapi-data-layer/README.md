# FastAPI in depth: Building the Data Layer

This chapter deals with the implementation of the data layer using SQLite and Python's database API, *DB-API*.

## DB-API

The DP-API interface is standard definition for interacting with a relational database.

Any driver satisfying this interface must at least provide an implementation for these functions:

+ Create a connection `conn` to the database using `connect()`.
+ Create a cursor `curs` using `conn.cursor()`.
+ Execute a SQL string `stmt` with `curs.execute(stmt)`.

In particular, `execute` runs allow for optional parameters:

+ `execute(stmt)` when no parameters are needed.
+ `execute(stmt, params)` with `params` being a sequence or dict.
+ `executemany(stmt, params_seq)`, when using multiple parameter groups.

There are multiple ways of specifying the parameters, and not all of them are supported by all database drivers. The following discusses these options:

| Type | Statement | Parameters |
| :--- | :-------- | :--------- |
| question mark | `name=? or country=?` | `(name, country)` |
| numeric | `name=:0 or country=:1` | `(name, country)` |
| format | `name=%s or country=%s` | `(name, country)` |
| named | `name=:name or country=:country` | `{"name": "name", "country": "country}` |
| pyformat | `name=%(name)s or country=%(country)s` | `{"name": "name", "country": "country}` |

For example, when using named-style parameters you'd do:

```python
stmt = """
  SELECT * FROM creature
   WHERE name=:name OR country=:country
"""
params = {"name": "yeti", "country": "CN"}
curs.execute(stmt, params)
```

For SQL `INSERT`, `DELETE`, and `UPDATE` statements, the returned value from `execute()` tells you how it worked.

For SQL `SELECT` statements, you have to iterate over returned data row(s) as Python tuples, with a fetch method:

+ `fetchone()` &mdash; returns one tuple, or `None`.
+ `fetchall()` &mdash; returns a sequence of tuples.
+ `fetchmany(num)` &mdash; returns up to `num` tuples.

## SQLite

Python includes support for SQLite database in the `sqlite3` module, which is part of the standard packages.

SQLite is actually a library, and storage is in a single file.

You can implement the data layer with `sqlite3` module. Apart from creating the data access packages for the creature and explorer, it is common to create a data initialization module `data/init.py`.

Because Python modules are singletons, they're only called once despite being imported multiple times. Thus, you can trust on `init.py` being called just once when the first import occurred.

```python
import os
from pathlib import Path
from sqlite3 import Connection, Cursor, connect

from cryptid.utils.log_config import get_logger

conn: Connection | None = None
curs: Cursor | None = None

def get_db(name: str | None = None, reset: bool = False):
    global conn, curs  # global will let us modify the value of those vars
    if conn:
        if not reset:
            return
        conn = None
    if not name:
        name = os.getenv("CRYPTID_SQLITE_DB")
        prj_root_dir = Path(__file__).resolve().parents[1]
        db_dir = prj_root_dir / "db"
        db_name = "cryptid.db"
        db_path = str(db_dir / db_name)
        name = os.getenv("CRYPTID_SQLITE_DB", db_path)
    conn = connect(name, check_same_thread=False)
    curs = conn.cursor()


get_db()
```

The data access module will then import the previous module and use the `curs` object to interact with the database:

```python
from model.explorer import Explorer

from cryptid.data.init import curs

if curs is not None:
    curs.execute(
        """
        CREATE TABLE IF NOT EXISTS explorer
            (name TEXT PRIMARY KEY,
             country TEXT,
             description TEXT)
        """
    )
else:
    raise TypeError("cursor not initialized")


def row_to_model(row: tuple) -> Explorer:
    name, country, description = row
    return Explorer(
        name=name, country=country, description=description
    )


def model_to_dict(creature: Explorer) -> dict:
    return creature.model_dump()


def get_one(name: str) -> Explorer:
    query = """
        SELECT * FROM explorer
         WHERE name = :name
    """
    params = {"name": name}
    curs.execute(query, params)
    row = curs.fetchone()
    return row_to_model(row)


def get_all() -> list[Explorer]:
    query = """
        SELECT * FROM explorer
    """
    curs.execute(query)
    rows = list(curs.fetchall())
    return [row_to_model(row) for row in rows]


def create(explorer: Explorer) -> Explorer:
    query = """
        INSERT INTO explorer
        VALUES (:name, :country, :description)
    """
    params = model_to_dict(explorer)
    curs.execute(query, params)
    return get_one(explorer.name)


def modify(name: str, explorer: Explorer) -> Explorer:
    query = """
        UPDATE explorer
           SET country = :country,
               name = :name,
               description = :description
         WHERE name = :name_orig
    """
    params = model_to_dict(explorer)
    params["name_orig"] = name
    _ = curs.execute(query, params)
    return get_one(explorer.name)


def delete(explorer: Explorer) -> bool:
    query = """
        DELETE FROM explorer
         WHERE name = :name
    """
    params = {"name": explorer.name}
    res = curs.execute(query, params)
    return bool(res)
```

With the data layer in place, you just need to wire the web layer to the service layer, and the service layer with the data layer instead of with the *fakes*.

As a side note, the redirection problems we were facing when sending a request to `/explorer` and `/creature` when using routers can be solved by decorating the corresponding endpoints with two URLs:

```python
@router.get("")
@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()
```

## Managing exceptions

It is a common practice to define custom exceptions for situations arising in the data layer, so that those are gracefully. In this case, errors occurring because we're trying to create duplicate data or trying to find non-persisted data are ocurring at the db level.

Because of that, it makes sense to define custom exceptions in the data package in a file named `/data/errors.py`:

```python
class MissingError(Exception):
    pass


class DuplicateError(Exception):
    pass


class InvalidStateError(Exception):
    pass
```

Then we can update our data access layer code to raise those exceptions when an *unhappy path* situation is detected.

```python
def get_one(name: str) -> Explorer:
    query = """
        SELECT * FROM explorer
         WHERE name = :name
    """
    params = {"name": name}
    if curs:
        curs.execute(query, params)
        row = curs.fetchone()
        if row:
            return row_to_model(row)
        else:
            raise MissingError(f"Explorer {name} not found")
    else:
        raise InvalidStateError("Cursor not initialized")
```

## Unit Tests

SQLite makes it very easy to write unit tests because it supports a completely in-memory mode when using `":memory:"` as the database location.

That allows you to create test functions for your data layer without requiring you to clean the results after each session execution.

We can configure this functionality with a small hack that sets the value `CRYPTID_SQLITE_DB` environment variable before importing the data access layer.

In the test programs we also use PyTest fixtures.

A PyTest fixture is a special function that helps you set up and manage the environment for your tests. In our case, we can use it to pass data to our tests.

```python
import os

import pytest

from cryptid.data.errors import DuplicateError, MissingError
from cryptid.model.explorer import Explorer

# Setting SQLite in-memory mode before importing the Data Layer
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from cryptid.data import explorer


@pytest.fixture
def sample() -> Explorer:
    return Explorer(
        name="Van Helsing",
        country="NL",
        description="Vampire slayer"
    )


def test_create(sample):
    got = explorer.create(sample)
    assert got == sample


def test_create_duplicate(sample):
    with pytest.raises(DuplicateError):
        explorer.create(sample)


def test_get_one_missing():
    with pytest.raises(MissingError):
        creature.get_one("Werewolf")
```

Note that a PyTest function will receive the result from a fixture automatically by simply declaring an argument that matches the fixture name. Otherwise, the fixture will not be provided (as in `test_get_one_missing`).

Note also that you can use `with` to write tests that expect exceptions to be raised.

We didn't make use of it, but with PyTest a fixture can be configured to have a particular scope:

+ Function scope &mdash; the fixture is called before every test function. This is the default.

+ Session scope &mdash; the fixture is called only once, at the beginning of the test file execution.

In the example above, the fixture uses the default function scope, so that the test functions get a brand new object as configured in the fixture.

On the other hand, because we're not resetting the database at the end of each test function execution, we're relying on the execution of the previous test functions (which is not a very good idea, as we cannot run the test functions individually).