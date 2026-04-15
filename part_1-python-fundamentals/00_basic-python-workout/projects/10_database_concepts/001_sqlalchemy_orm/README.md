# SQLAlchemy basics

+ [High-level architecture](#high-level-architecture)
+ [SQLAlchemy: Core API basics](#sqlalchemy-core-api-basics)
    + [Establishing connectivity: the `Engine`](#establishing-connectivity-the-engine)
    + [Working with transactions: `Engine.connect()`, `Connection.commit()` and `Engine.begin()`](#working-with-transactions-engineconnect-connectioncommit-and-enginebegin)
    + [Fetching rows: the `Result` object](#fetching-rows-the-result-object)
    + [Sending (bound) parameters](#sending-bound-parameters)
    + [Creating DB objects: The `MetaData` object](#creating-db-objects-the-metadata-object)
        + [Creating `Table` objects programmatically](#creating-table-objects-programmatically)
        + [Emitting DDL to the DB](#emitting-ddl-to-the-db)
        + [Using reflection to generate `Table` objects from existing DB tables](#using-reflection-to-generate-table-objects-from-existing-db-tables)
    + [Using INSERT statements](#using-insert-statements)
        + [Inserting data from other tables](#inserting-data-from-other-tables)
        + [INSERT...RETURNING](#insertreturning)
        + [INSERT...FROM SELECT](#insertfrom-select)
    + [Using SELECT statements](#using-select-statements)
        + [Using LABEL](#using-label)
        + [Selecting with textual column expressions: `text()`](#selecting-with-textual-column-expressions-text)
        + [Using `literal_column()`](#using-literal_column)
        + [The WHERE clause](#the-where-clause)
            + [Using AND and OR conjunctions](#using-and-and-or-conjunctions)
        + [Using `filter_by()` for simple equality comparisons](#using-filter_by-for-simple-equality-comparisons)
        + [JOINs](#joins)
            + [A gentle refresher on JOINs](#a-gentle-refresher-on-joins)
                + [INNER JOIN (default JOIN)](#inner-join-default-join)
                + [LEFT OUTER JOIN](#left-outer-join)
                + [RIGHT OUTER JOIN](#right-outer-join)
                + [FULL OUTER JOIN](#full-outer-join)
            + [Explicit FROM clauses and JOIN](#explicit-from-clauses-and-join)
                + [Setting the ON clause](#setting-the-on-clause)
        + [ORDER BY](#order-by)
        + [Aggregate functions with GROUP BY / HAVING](#aggregate-functions-with-group-by--having)
        + [Using aliases](#using-aliases)
        + [Non-scalar subqueries](#non-scalar-subqueries)
        + [CTEs](#ctes)
        + [Scalar subqueries](#scalar-subqueries)
            + [Correlated subqueries and LATERAL correlation](#correlated-subqueries-and-lateral-correlation)
        + [UNION, UNION ALL and other set operations](#union-union-all-and-other-set-operations)
        + [EXISTS subqueries](#exists-subqueries)
        + [Working with SQL functions](#working-with-sql-functions)
            + [Using window functions](#using-window-functions)
            + [Special modifiers WITHIN GROUP, FILTER](#special-modifiers-within-group-filter)
            + [Table-valued functions](#table-valued-functions)
            + [Column valued functions: table-valued functions as a scalar column](#column-valued-functions-table-valued-functions-as-a-scalar-column)
        + [Data casts and type coercion](#data-casts-and-type-coercion)
            + [`type_coerce()`: a Python-only cast](#type_coerce-a-python-only-cast)
    + [Using UPDATE and DELETE statements](#using-update-and-delete-statements)
        + [Using UPDATE](#using-update)
            + [Correlated updates](#correlated-updates)
            + [UPDATE...FROM](#updatefrom)
    + [Using DELETE](#using-delete)
        + [Getting affected row count from UPDATE, DELETE](#getting-affected-row-count-from-update-delete)
        + [Using RETURNING with UPDATE, DELETE](#using-returning-with-update-delete)
    + [Closing a session](#closing-a-session)
+ [SQLAlchemy: ORM basics](#sqlalchemy-orm-basics)
    + [Working with DB metadata in ORM](#working-with-db-metadata-in-orm)
    + [Declaring mapped classes](#declaring-mapped-classes)
    + [Using SELECT statements in ORM](#using-select-statements-in-orm)
        + [Getting the first result with `first()` and `ScalarResult`](#getting-the-first-result-with-first-and-scalarresult)
        + [Getting all the results with `all()`](#getting-all-the-results-with-all)
        + [Combining multiple entities](#combining-multiple-entities)
        + [ORDER BY in ORM](#order-by-in-orm)
        + [Aggregate functions in ORM](#aggregate-functions-in-orm)
        + [ORM entity aliases](#orm-entity-aliases)
        + [ORM entity subqueries](#orm-entity-subqueries)
        + [ORM CTEs](#orm-ctes)
        + [Selecting ORM entities from unions](#selecting-orm-entities-from-unions)
    + [Inserting rows using the ORM Unit of Work pattern](#inserting-rows-using-the-orm-unit-of-work-pattern)
        + [Creating objects representing rows](#creating-objects-representing-rows)
        + [Adding objects to a `Session`](#adding-objects-to-a-session)
        + [Flushing](#flushing)
        + [Getting objects by primary key from the identity map](#getting-objects-by-primary-key-from-the-identity-map)
        + [Committing](#committing)
    + [Updating ORM objects using the Unit of Work pattern](#updating-orm-objects-using-the-unit-of-work-pattern)
    + [Deleting ORM objects using the Unit of Work pattern](#deleting-orm-objects-using-the-unit-of-work-pattern)
    + [Bulk / Multirow INSERT, upsert, UPDATE and DELETE](#bulk--multirow-insert-upsert-update-and-delete)
    + [Rolling back](#rolling-back)
    + [Closing a session](#closing-a-session)
    + [Working with relationships](#working-with-relationships)
        + [Persisting and loading relationships](#persisting-and-loading-relationships)
        + [Cascading objects into the session](#cascading-objects-into-the-session)
        + [Loading relationships](#loading-relationships)
        + [Using relationships in queries](#using-relationships-in-queries)
        + [Using relationships in JOINs](#using-relationships-in-joins)
        + [Loader strategies](#loader-strategies)
            + [Selectin load](#selectin-load)
            + [Joined load](#joined-load)
            + [Explicit join + eager load](#explicit-join--eager-load)
            + [Raise load](#raise-load)

+ [Asyncio integration](#asyncio-integration)
    + [Async Core API](#async-core-api)
    + [Async ORM](#async-orm)
        + [Using AsyncSession with concurrent tasks](#using-asyncsession-with-concurrent-tasks)
        + [Preventing implicit I/O when using `AsyncSession`](#preventing-implicit-io-when-using-asyncsession)

+ [Alembic](#alembic)
    + [The migration environment](#the-migration-environment)
        + [Editing the `.ini` file](#editing-the-ini-file)
        + [Using `pyproject.toml` for configuration](#using-pyprojecttoml-for-configuration)
    + [Creating a migration script](#creating-a-migration-script)
    + [Running your first migration](#running-your-first-migration)
    + [Running your second migration](#running-your-second-migration)
    + [Partial revision identifiers](#partial-revision-identifiers)
    + [Relative migration identifiers](#relative-migration-identifiers)
    + [Getting information](#getting-information)
    + [Downgrading](#downgrading)
    + [Auto generating migrations](#auto-generating-migrations)
        + [What does `--autogenerate` detect and what does not detect?](#what-does---autogenerate-detect-and-what-does-not-detect)
        + [Applying post processing and python code formatters to generated revisions](#applying-post-processing-and-python-code-formatters-to-generated-revisions)
    + [Running checks before the upgrade operation](#running-checks-before-the-upgrade-operation)
    + [The "offline mode"](#the-offline-mode)
    + [Data migration considerations](#data-migration-considerations)
        + [Small data](#small-data)
        + [Separate migration script](#separate-migration-script)
        + [Online migration](#online-migration)



## High-level architecture

The SQLAlchemy SQL toolkit and Object Relationship Mapper (ORM) is a comprehensive set of tools for working with databases in Python.

![SQLAlchemy](pics/001_sqlalchemy-app-arch.png)

SQLAlchemy is presented as two distinct APIs:

+ **Core**: SQL, database integration, and description services, including the SQL Expression Language.

    The SQL Expression Language provides a system of constructing SQL expressions represented by composable objects, which can be executed against a target DB within the scope of a specific transaction, returning a result set.

+ **ORM**: Builds upon the core to enable working with a domain model object mapped to a DB schema.

| NOTE: |
| :---- |
| Working with Core and SQL Expression Language is command oriented and schema-centric, while ORM is state oriented. |

The two APIs have a lot of intersections and similarities, but from the learning perspective, you will have an easier time learning the basics of core in the [SQLAlchemy: Core API basics](#sqlalchemy-core-api-basics) section, and then dealing with ORM in the [SQLAlchemy: ORM basics](#sqlalchemy-orm-basics) section.

## SQLAlchemy: Core API basics

### Establishing connectivity: the `Engine`

The `Engine` is an object that acts as a central source of connections to a particular DB, providing both a factory and a holding space called *connection pool* for those DB connections.

The `Engine` is typically a global object created just once for a particular DB server, and configured using a URL string which describes how it should connect to the DB.

For example:

```python
from sqlalchemy import create_engine

engine = create_engine("sqlite+pysqlite:///:memory", echo=True")
```

where:

+ `sqlite+pysqlite` indicates that you will be using the modern pysqlite interface for sqlite3, instead of the default DBAPI.
+ `/:memory:` indicates you will be using the in-memory option, which won't create any file. Something like `/app.db` could have been used instead.
+ `echo=True` instructs the engine to log the SQL statements it emits.

### Working with transactions: `Engine.connect()`, `Connection.commit()` and `Engine.begin()`

You can use the `Engine` object to obtain a `Connection` object which will allow you to connect to the DB.

The `Connection` object is how all interaction with the DB is done. It must be used with the *Context Manager* protocol (`with ... as conn`) to ensure proper release of the DB connections.

The following snippet illustrates how to issue a SQL statement to the DB using the `engine.connect()` method. Note the `text()` is used to wrap the SQL statement, and `conn.execute()`

```python
from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
with engine.connect() as conn:
    result = conn.execute(text("select 'hello, world!'"))
```

By default, when a connection is released a ROLLBACK will be issued end the transaction and undo the changes.

To commit the data you've altered within a transaction, you'll need to either:
+ use the *commit as you go* approach explicitly using `Connection.commit()`.
+ use the *begin once* approach, using `engine.begin()` which automatically commits the changes if no errors are found.

The following snippet illustrates both approaches:

```python
# commit as you go
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("CREATE TABLE some_table (x int, y int) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()

# begin once
with engine.begin() as conn:
    conn.execute(
        text("CREATE TABLE some_table (x int, y int) VALUES (:x, :y)"),
        [{"x": 3, "y": 9}, {"x": 4, "y": 16}],
    )
```

| NOTE: |
| :---- |
| You should prefer the *begin once*, as it's cleaner and more expressive. |

### Fetching rows: the `Result` object

The following snippet illustrates how to iterate over the rows fetched from a table:

```python
with engine.conn() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x} y: {row.y}")
```

See how the `Result` object returned by `Connection.execute()` represents an iterable object of result rows, and that each individual column from the result set can be accessed through the name as if it were a property.

Alternatively, you can use `Result.all()` and `Result.first()` to materialize the whole set of returned rows in a list, or the first row without iterating over the result.

There are multiple ways of accessing `Row` objects:

+ Attribute name:

    ```python
    result = conn.execute(text("select x, y from some_table"))
    for row in result:
        x = row.x
        y = row.y
    ```


+ Tuple assignment:

    ```python
    result = conn.execute(text("select x, y from some_table"))
    for x, y in result:
        ...
    ```

+ Integer index:

    ```python
    result = conn.execute(text("select x, y from some_table"))
    for row in result:
        x = row[0]
        y = row[1]
    ```


+ Mapping access:

    ```python
    result = conn.execute(text("select x, y from some_table"))
    for row_dict in result.mappings():
        x = row_dict["x"]
        y = row_dict["y"]
    ```

### Sending (bound) parameters

The syntax for sending (bound) parameters to a textual query is:

```python
# sending single parameter
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})

# sending multiple parameters
with engine.connect() as conn:
    conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"), [{"x":11, "y": 22}, {"x": 13, "y": 14}])
```

| NOTE: |
| :---- |
| Always use bound parameters! Never stringify parameters into the actual SQL query as you'll be opening the door for SQL injection attacks. |


| EXAMPLE: |
| :------- |
| See [SQL Alchemy: Basics](001_sqlalchemy_core_basics/README.md) for a runnable example. |

### Creating DB objects: The `MetaData` object

The `MetaData` object is a sort of *holder* where you will place places all your tables, columns, and related DB objects.

Programmatically, you can think of this `Metadata` object as a façade around a dict storing `Table` objects keyed by their string name.

```python
from sqlalchemy import Metadata

metadata_obj = MetaData()
```

You sould typically have a single `MetaData` instance for the entire application, represented as a module-level variable defined in a `dbschema.py` file or similar.

There might be situations when having multiple `MetaData` collections might be useful to group tables that are related together. However, in practice, it's better to have them in a single `MetaData` object for various reasons, such as correct management of dependencies when creating them, etc.

#### Creating `Table` objects programmatically

The following snippet illustrates how to create a `Table` object that represents a table in the DB:

```python
from sqlalchemy import Table, Column, Integer, String

metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)
```

Note that the `id` column defines that column as the table's primary key using the parameter `primary_key=True`.

By contrast, declaring a foreign key constraint, requires you to use the `ForeignKey()` constructor.

| NOTE: |
| :---- |
| A foreign key constraint declares a relationship between two columns from two different tables. |


```python
from sqlalchemy import ForeignKey

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)
```

Note that by default, columns are nullable (as in SQL), so you'll have to use `nullable=False` to declare a NOT NULL column.


#### Emitting DDL to the DB

The `MetaData` object provides a `create_all()` and `drop_all()` methods that you can use to generate all the objects held by a `MetaData` instance.

```python
# create all the tables
metadata_obj.create_all(engine)

# drop all the tables
metadata_obj.drop_all(engine)
```


The statements will be issued in the correct order.


| NOTE: |
| :---- |
| `MetaData`'s CREATE/DROP features are useful for test suites, but for production support you should rely on migration tools such as [Alembic](https://alembic.sqlalchemy.org/). |


#### Using reflection to generate `Table` objects from existing DB tables

Reflection refers to the capability of generating `Table` and their related object by reading the current state of a DB.

SQLAlchemy supports reflection by way of `autoload_with=engine` parameter:

```python
some_table = Table("some_table", metadata_obj, autoload_with=engine)
```

### Using INSERT statements

SQL INSERT statements are used to add new rows to your tables.

SQLAlchemy provides the `insert()` function that returns an `Insert` object that represents the underlying INSERT statement, which will ultimately add new rows to your tables.

The simplest way to use it is:

```python
from sqlalchemy import insert

stmt = (
    insert(user_table)
    .values(
        name="spongebob",
        fullname="Spongebob Squarepants",
    )
)

# INSERT using commit as you go
with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()
```

You can inspect the internals of an statement in several different ways:

```python
# print the SQL statement the stmt represents
print(stmt)

# get the compiled form of the stmt
compiled_stmt = stmt.compile()

# get the parameter information used in the stmt
print(compiled.params)
```

In general, the INSERT statement does not return any rows. Some DBs may return the inserted primary key if a single row was inserted. That can be accessed using `result.inserted_primary_key`:

```python
print(f"Inserted user id: {result.inserted_primary_key}")
```


Also, you can send multiple rows to be inserted using:

```python
with engine.connect() as conn:
    result = conn.execute(
        insert(user_table),
        [
            {"name": "sandy", "Sandy Cheeks"},
            {"name": "patrick", "Patrick Star"},
        ],
    )
    conn.commit()
```

| NOTE: |
| :---- |
| When passing a list of dictionaries to `conn.execute()` only the first one is scanned to decide which are the values that you intend to populate. |


#### Inserting data from other tables

In an INSERT statement, you can use data from other tables using a technique known as scalar subqueries. An scalar subquery is a query you can encode in the `values()` part of your query the pulls information from another table. It is called *scalar* because instead of returning a `Row` object, it returns the raw value selected.

The following snippet illustrates how to populate the `address` table by pulling the `id`'s from the `user_account` table, so that the foreign key relationship is correctly populated.

The snippet also makes use of `bindparam()` which allows you to refer to dinamically bound parameters:

```python
from sqlalchemy import select, bindparam

scalar_subq = (
    select(user_table.c.id)
    .where(user_table.c.id == bindparam("username"))
    .scalar_subquery()
)

with engine.connect() as conn:
    result = conn.execute(
        insert(address_table)
        .values(user_id=scalar_subq),
        [
            {"username": "patrick", "email_address": "patrick@example.com"},
            {"username": "sandy", "email_address": "sandy@example.com"},
        ]
    )
    conn.commit()
```

Please note that the `values()` function is only used to populate the `user_id`, while the list of values provided to `execute()` are used both for the subquery and the population of the other `address` related columns.

#### INSERT...RETURNING

The RETURNING clause in SQL lets you specify what are the values you'd like to be returned after issuing an INSERT statement.

SQLAlchemy supports that with `returning()`:

```python
insert_stmt = (
    insert(address_table)
    .returning(
        address_table.c.id,
        address_table.c.email_address
    )
)
```

#### INSERT...FROM SELECT

The INSERT... FROM SELECT statement is used to insert data into a table from some other part of the DB directly, without actually fetching and re-sending the data from the client.

The following snippet illustrates how to do so in SQLAlchemy. The code populates the `address_table` by reading the `user_account` table.

```python
select_stmt = select(user_table.c.id, user_table.c.name + "@example.com")

insert_stmt = (
    insert(address_table)
    .from_select(
        ["user_id", "email_address"],
        select_stmt
    )
)
```

Note that you need to specify the columns that will be populated from the query. The `select_stmt` must provide those values in the given order (i.e., first fetched column for `user_id`, second one for `email_address`).

### Using SELECT statements

The SQL SELECT statements are used to fetch rows from one or more DB tables.

The `select()` function generates a `Select` object, which is used to represent and ultimately run SELECT queries.

The `select()` function allows you to build up a SELECT statement in phases by way of chaining additional calls to the result of invoking `select()`. Each method adds more state in the `Select` object.

For example:

```python
# SELECT * FROM table
stmt = select(user_table)

# SELECT * FROM table WHERE ...
stmt = (
    select(user_table)
    .where(user_table.c.name == "spongebob")
)
```

To retrieve the results of the query you can iterate over the `Result` object, or materialize the whole or a part of the resulting rows using `Result.all()` or `Result.first()`.


```python
with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)
```


You can fetch individual columns from the table/tables using the `Table.c` accessor:

```python
# SELECT name, fullname FROM user_account
stmt = select(user_table.c.name, user_table.c.fullname)

# SELECT name, fullname FROM user_account
stmt = select(user_table.c["name", "fullname"])
```

Although the JOIN operations will be discussed in detail in a separate subsection, it's important to note that you can combine multiple tables and/or columns from other specific tables:

```python
with engine.connect() as conn:
    rows = conn.execute(
        select(user_table.c.name, address_table)
        .where(user_table.c.id == address_table.c.user_id)
        .order_by(address_table.c.id)
    )
    .all()
```

Note also that `order_by()` is used to get the results in a specific order.

#### Using LABEL

The LABEL clause (SQL `AS`) assigns an alias to a column expression in a SELECT query, controlling the name used to access that column in the result set.

SQLAlchemy provides the `label()` method to give a name to a column or expression, so that you can refer to it in other parts of the query.

```python
stmt = (
    select(
        ("Username: " + user_table.c.name).label("username"),
    )
    .order_by(user_table.c.name)
)

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(f"{row.username=}")
```

Note how you can mention the label name where iterating over the resulting rows.

#### Selecting with textual column expressions: `text()`

The `text()` function comes in handy when you want to manufacture arbitrary SQL block inside of a statement.

This might happen when you need to write some constant expression, or when it'd be quicker to write SQL than relying on SQLAlchemy constructs:

```python
from sqlalchemy import text

stmt = (
    select(
        text("'some phrase'"),
        user_table.c.name
    )
    .order_by(user_table.c.name)
)
```

#### Using `literal_column()`

`literal_column()` is similar to `text()` except that instead of representing arbitrary SQL, it explicitly represents a single column, which makes it much more specific, and there preferred, over `text()`:

```python
from sqlalchemy import literal_column

stmt = (
    select(
        literal_column("'some phrase'").label("p"),
        user_table.c.name,
    )
    .order_by(user_table.c.name)
)

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(f"{row.p}, {row.name}")
```

#### The WHERE clause

The SQL WHERE clause is used to filter the columns affected when issuing a statement.

SQLAlchemy provides the `where()` method that you can use to compose SQL expressions using standard Python operators:

```python
stmt = (
    select(user_table)
    .where(user_table.c.name == "squidward")
)

stmt = (
    select(address_table)
    .where(address_table.c.user_id > 10)
)
```

To produce multiple expressions joined by AND, you can either use `where()` multiple times or pass multiple expressions to `where()`:

```python
# AND using multiple where()
stmt = (
    select(address_table.c.email_address)
    .where(user_table.c.name == "squidward")
    .where(address_table.c.user_id == user_table.c.id)
)

# AND passing multiple parameters to where()
stmt = (
    select(address_table.c.email_address)
    .where(
        user_table.c.name == "squidward",
        address_table.c.user_id == user_table.c.id
    )
)
```

##### Using AND and OR conjunctions

SQLAlchemy provides `and_()` and `or_()` functions to allow you write complex AND/OR conjunctions in your queries:

```python
from sqlalchemy import and_, or_

stmt = (
    select(address_table.c.email)
    .where(
        and_(
            or_(
                user_table.c.name == "squidward",
                user_table.c.name == "sandy",
            ),
            address_table.c.user_id == user_table.c.id,
        ),
    )
)
```

#### Using `filter_by()` for simple equality comparisons

You can use `Select.filter_by()` for simple equality comparisons against a single table.

`filter_by()` accepts keyword arguments that match to column keys. It will filter agains the leftmost FROM clause:

```python
stmt = (
    select(user_table)
    .filter_by(
        name="spongebob",
        fullname="Spongebob Squarepants",
    )
)
```

#### JOINs

##### A gentle refresher on JOINs

A JOIN combines rows from two or more tables into a single result set based on a related column between them, typically a foreign key relationship.

In SQL there are four types of JOINs:
+ INNER JOIN
+ LEFT OUTER JOIN
+ RIGHT OUTER JOIN
+ FULL OUTER JOIN

To understand the differences between them, let's assume we have two tables:
+ Table `a` with columns `k`, and `v`.

    | k | v |
    | :- | :- |
    | 1 | "uno" |
    | 2 | "dos" |
    | 3 | "tres" |


+ Table `b` with columns `k`, and `w`.

    | k | w |
    | :- | :- |
    | 1 | "one" |
    | 2 | "two" |
    | 4 | "four" |

There are no foreign key relationships between the tables, but they can be joined by `k`.

###### INNER JOIN (default JOIN)

In an INNER JOIN (default JOIN), the result will contain all possible pairs `(k, (v, w))` from the left-hand and right-hand tables that have the same keys (i.e., `k` values).

There will no records in the result for the keys that exist in only one of the tables.

```sql
    SELECT *
      FROM a
INNER JOIN b
        ON a.k = b.k
```

| `a.k` | `v`   | `b.k` | `w`   |
| :---- | :---- | :---- | :---- |
| 1     | uno   | 1     | one   |
| 2     | dos   | 2     | two   |

| NOTE: |
| :---- |
| An INNER JOIN is the same as the implicit join you do in `SELECT * FROM a, b WHERE a.k = b.k`. However, this syntax is discouraged, as it's harder to read and less explicit than its counterpart. |

###### LEFT OUTER JOIN

A LEFT OUTER JOIN returns all rows from the left table, and the matching rows from the right table, so that you'll get `(k, (v, w | [null]))`. Where there is no match in the right table, the right-side columns are filled with `[null]`.

Rows that exist only in the right table are not included.

```sql
         SELECT *
           FROM a
LEFT OUTER JOIN b
             ON a.k = b.k
```

| `a.k` | `v`   | `b.k`  | `w`    |
| :---- | :---- | :----- | :----- |
| 1     | uno   | 1      | one    |
| 2     | dos   | 2      | two    |
| 3     | tres  | [null] | [null] |


###### RIGHT OUTER JOIN

A RIGHT OUTER JOIN returns all rows from the right table, and the matching rows from the left table. Where there is no match in the left table, the left-side columns are filled with `[null]`, so you'll get `(k, (v | [null], w))`.

Rows that exist only in the left table are not included.

```sql
          SELECT *
            FROM a
RIGHT OUTER JOIN b
             ON a.k = b.k
```

| `a.k`  | `v`    | `b.k`  | `w`    |
| :----- | :----- | :----- | :----- |
| 1      | uno    | 1      | one    |
| 2      | dos    | 2      | two    |
| [null] | [null] | 4      | four   |


It must be noted that a RIGHT OUTER JOIN is exactly the same as a LEFT OUTER JOIN in which the tables have been swapped:

```sql
/* LEFT OUTER JOIN with tables swapped */
          SELECT *
            FROM b
 LEFT OUTER JOIN a
             ON a.k = b.k
```

| `b.k`  | `w`    | `a.k`  | `v`    |
| :----- | :----- | :----- | :----- |
| 1      | one    | 1      | uno    |
| 2      | two    | 2      | dos    |
| 4      | four   | [null] | [null] |


###### FULL OUTER JOIN

A FULL OUTER JOIN returns **all rows from both tables**. Where there is no match on either side, the missing columns are filled with `NULL`, so that result set will be `(k, (v | [null]), (w | [null]))`.

It is the union of LEFT and RIGHT OUTER JOINs: every row from `a` and every row from `b` appears at least once in the result.

```sql
          SELECT *
            FROM a
 FULL OUTER JOIN b
             ON a.k = b.k
```

| `a.k`  | `v`    | `b.k`  | `w`    |
| :----- | :----- | :----- | :----- |
| 1      | uno    | 1      | one    |
| 2      | dos    | 2      | two    |
| 3      | tres   | [null] | [null] |
| [null] | [null] | 4      | four   |

##### Explicit FROM clauses and JOIN

The SQL FROM clause identifies the tables you are selecting data from.

In general, SQLAlchemy will be able to infer the FROM clause from your code by inspecting the `Select` object:

```python
# SELECT name FROM user_account
stmt = select(user_table.c.name)

# SELECT user_account.name, address.email_address
#   FROM user_account, address
stmt = select(user_table.c.name, address_table.c.email_address)
```

However, you will find situations in which you need to explicitly declare what tables you need to join together. In those case, you can use `join_from()` to indicate both the left and right side of the JOIN explicitly:

```python
# SELECT user_account.name, address.email_address
#   FROM user_account
#   JOIN address
#     ON user_account.id = address.user_id
stmt = (
    select(user_table.c.name, address_table.c.email)
    .join_from(user_table, address_table)
)
```

SQLAlchemy also provides the `join()` method to indicate only the right-hand side of the JOIN. In those cases, SQLAlchemy will infer the left-hand side:

```python
# SELECT user_account.name, address.email_address
#   FROM user_account
#   JOIN address
#     ON user_account.id = address.user_id
stmt = (
    select(user_table.c.name, address_table.c.email)
    .join(address_table)
)
```

Note that SQLAlchemy inferral capabilities won't stop at identifying the FROM clause in your joins, but will also attempt to craft the `ON` clause based on the foreign key definitions.


However, there'll be situations in which SQLAlchemy won't be able to infer the table/tables involved in the SELECT statement. In those cases, you can use `select_from()` to explicitly identify the tables to be used in the FROM clause:

```python
from sqlalchemy import func

# SELECT count(*)
#   FROM user_account
stmt = (
    select(func.count("*"))
    .select_from(user_table)
)
```

###### Setting the ON clause

There will be situations in which SQLAlchemy won't be able to craft the ON clause for you (e.g., foreign keys might not be present). In those cases, you will be able to identify the ON clause explicitly sending extra parameters to `join_from()` and `join()`:

+ `join_from(from_, target, onclause)`
+ `join(target, onclause)`

```python
# SELECT address.email_address
#   FROM user_table
#   JOIN user_account
#     ON address.user_id = user_account.id
stmt = (
    select(address_table.c.email_address)
    .join(
        user_table,
        address_table.c.user_id == user_table.c.id,
    )
)
```

Additionally, both `join_from()` and `join()` accept extra keyword arguments `isouter` and `full` to render LEFT OUTER JOIN and FULL OUTER JOIN respectively:

+ `join_from(from_, target, onclause, isouter, full)`
+ `join(target, onclause, isouter, full)`

```python
# SELECT *
#   FROM num_esp
# LEFT OUTER JOIN num_eng
#              ON num_esp.id = num_eng.id
stmt = (
    select(user_table)
    .join(address_table, isouter=True)
)

#          SELECT *
#            FROM num_esp
# FULL OUTER JOIN num_eng
#              ON num_esp.id = num_eng.id
stmt = (
    select(user_table)
    .join(address_table, full=True)
)
```

SQLAlchemy also provides the `outerjoin()` which is equivalent to `join(..., isouter=True)`:

```python
# SELECT *
#   FROM num_esp
# LEFT OUTER JOIN num_eng
#              ON num_esp.id = num_eng.id
stmt = (
    select(user_table)
    .outerjoin(address_table)
)
```

Note that there's no method for a RIGHT OUTER JOIN. If you need to issue a RIGHT OUTER JOIN, you can write a LEFT OUTER JOIN and swap the left-hand and right-hand side tables.


#### ORDER BY

The ORDER BY clause sorts the rows in a query's result set by one or more columns, either ascending (`ASC`, the default) or descending (`DESC`).

SQLAlchemy provides the `order_by()` method that accepts one or more expressions to build the corresponding ORDER BY clause, and lets you choose ascending or descending ordering:

```python
# ORDER BY name
stmt = (
    select(user_table)
    .order_by(user_table.c.name)
)

# ORDER BY name DESC
stmt = (
    select(user_table)
    .order_by(user_table.c.name.desc())
)
```

#### Aggregate functions with GROUP BY / HAVING

In SQL, aggregate functions (counting, averages, min, max, ...) allow column expressions across multiple rows to be aggregated together to produce a single result.

For example, to render the SQL COUNT() agains the `user_account.id` column you'd do:

```python
from sqlalchemy import func

count_fn = func.count(user_table.c.id)

stmt = select(count_fn)
```

When using aggregate functions, the GROUP BY clause allows you to partition the rows in the result set into group, where aggregate functions will be applied to each group individually.

The HAVING clause is then used as a sort of WHERE clause, except that it will filter out rows based on aggregated values rather than direct row contents.

In SQLAlchemy, this is implemented with `group_by()` and `having()`. As an example, the following query selects the `name` field and the count of records in the `address` table for that user, locating filtering out those users that have more than one address:

```python
stmt = (
    select(user_table.c.name, func.count(address.id).label("count"))
    .join(address_table)
    .group_by(user_table.c.name)
    .having(func.count(address_table.c.id) > 1)
)
```

Some DBs provide the capability to ORDER BY or GROUP BY by an expression that is already stated in the COLUMNS clause, without re-stating the expression. You can do so in SQLAlchemy too:

```python
stmt = (
    select(
        address_table.c.user_id,
        func.count(address_table.c.id).label("num_addresses")
    )
    .group_by("user_id")
    .order_by("user_id", desc("num_addresses"))
)
```

Note that you need pass the column as a text string (e.g., "user_id") rather than a typed expressions such as `address_table.c.user_id`.


#### Using aliases

SQL aliases (AS clause) let you supply an alternative name to a table or subquery from which it can be referenced in the statement. This technique is particularly useful when you are selecting from multiple tables using JOINs and you're referring to the same table multiple times.

For example, the following query returns all unique pairs of user names by joining the `user_account` table with itself:

```python
user_alias_1 = user_table.alias()
user_alias_2 = user_table.alias()

stmt = (
    select(user_alias_1.c.name, user_alias_2.c.name)
    .join_from(
        user_alias_1,
        user_alias_2,
        user_alias_1.c.id > user_alias_2.c.id
    )
)
```

#### Non-scalar subqueries

In SQL a subquery is a SELECT statement that is rendered within parenthesis and placed within the context of an enclosing statement. Those are most commonly used in SELECT statements, but not always.

There are [*scalar*](#scalar-subqueries), and *non-scalar* subqueries. *Non-scalar* subqueries return a result set with rows (as if they were tables).

In SQLAlchemy, non-scalar subqueries are identified with the `subquery()` method:

```python
subq = (
    select(
        func.count(address_table.c.id).label("count"),
        address_table.c.user_id,
    )
    .group_by(address_table.c.user_id)
    .subquery()
)
```

A `Subquery` object behaves like any other FROM object (e.g., like a `Table`) and even produced the `Subquery.c` column accessor:

```python
stmt = (
    select(
        user_table.c.name,
        user_table.c.fullname,
        sub.c.count
    )
    .join_from(user_table, subq)
)
```

#### CTEs

Common Table Expressions (CTEs) are named, temporary result sets defined with a `WITH` clause at the top of a query, making complex queries easier to read by breaking them into reusable, self-contained building blocks.

In SQLAlchemy, CTEs are virtually identical to `Subquery` constructs. When using CTEs, you can use the resulting object as a FROM element (as in subqueries), but the rendered statement has a different syntax.

```python
cte_subq = (
    select(
        func.count(address_table.c.id).label("count"),
        address_table.c.user_id,
    )
    .group_by(address_table.c.user_id)
    .cte()
)

# WITH address_count_cte AS (
#   SELECT address.user_id AS user_id,
#          count(address.id) AS address_count
#     FROM address GROUP BY address.user_id)
# SELECT user_account.name,
#        user_account.fullname,
#        address_count_cte.address_count
#   FROM user_account
#   JOIN address_count_cte
#     ON user_account.id = address_count_cte.user_id
stmt = (
    select(
        user_table.c.name,
        user_table.c.fullname,
        sub.c.count
    )
    .join_from(user_table, subq)
)
```

#### Scalar subqueries

In SQL a subquery is a SELECT statement that is rendered within parenthesis and placed within the context of an enclosing statement. Those are most commonly used in SELECT statements, but not always.

There are *scalar* and [*non-scalar*](#non-scalar-subqueries) subqueries. *Scalar* subqueries return exactly zero or one row and exactly one column.

The subquery is then used in the COLUMNS or WHERE clause of an enclosing SELECT statement and is different than a regular subquery in that it is not used in the FROM clause.

Scalar subqueries are often, but not necessarily, used with aggregate functions.

SQLAlchemy represents the scalar subquery using the `ScalarSelect` construct, by explicitly making use of the `subquery()` method:

```python
# (SELECT count(address.id) AS count_1
#    FROM address, user_account
#   WHERE address.user_id = user_account.id)
subq = (
    select(func.count(address_table.c.id))
    .where(user_table.c.id == address_table.c.user_id)
    .scalar_subquery()
)
```

The subquery can then be used with SQL expression:

```python
subq == 5
```

##### Correlated subqueries and LATERAL correlation

A correlated subquery is a scalar subquery that refers to a table in the enclosing SELECT statement.


Simple correlated queries will usually do the right thing that's intended, but in some cases, you might need to explictly use `correlate()`:

```python
subq = (
    select(func.count(address_table.c.id))
    .where(user_table.c.id == address_table.c.user_id)
    .scalar_subquery()
    .correlate(user_table)
)
```

The statement then can return the data for this column:

```python
stmt = (
    select(
        user_table.c.name,
        address_table.c.email_address,
        sub.label("address_count"),
    )
    .join_from(user_table, address_table)
    .order_by(user_table.c.id, address_table.c.id)
)
```

LATERAL correlation is a special sub-category of SQL correlation which allows a selectable unit to refer to another selectable unit within a single FROM clause.

| NOTE: |
| :---- |
| This extremely special case is only known to be supported by recent versions of PostgreSQL. |

SQLAlchemy supports this using `Select.lateral()`, which creates a `Lateral` object.

```python
subq = (
    select(
        func.count(address_table.c.id).label("address_count"),
        address_table.c.email_address,
        address_table.c.user_id,
    )
    .where(user_table.c.id == address_table.c.user_id)
    .lateral()
)
stmt = (
    select(
        user_table.c.name,
        subq.c.address_count,
        subq.c.email_address
    )
    .join_from(user_table, subq)
    .order_by(user_table.c.id, subq.c.email_address)
)
```

#### UNION, UNION ALL and other set operations

In SQL, SELECT statements can be merged together using the UNION or UNION ALL operations, which produces the set of all rows produced by one or more statements together.

| NOTE: |
| :---- |
| The difference between UNION and UNION ALL is that the latter deduplicates the result set (i.e., dupes are eliminated). |

Less common are the INTERSECT, EXCEPT, INTERSECT ALL, and EXCEPT ALL.

SQLALchemy's `Select` construct supports all them through the functions:

+ `union()` and `union_all()`
+ `insersect()` and `intesect_all()`
+ `except_()` and `except_all()`

```python
from sqlalchemy import union_all

stmt_1 = (
    select(user_table)
    .where(user_table.c.name == "sandy")
)

stmt_2 = (
    select(user_table)
    .where(user_table.c.name == "spongebob")
)

u = union_all(stmt_1, stmt_2)
```

The `union_all` is a `CompoundSelect` object. This type of object can be used as a subquery:

```python
u_subq = u.subquery()

stmt = (
    select(
        u_subq.c.name,
        address_table.c.email_address,
    )
    .join_from(address_table, u_subq)
    .order_by(u_subq.c.name, address_table.c.email_address)
)
```

#### EXISTS subqueries

The SQL EXISTS keyword is an operator that is used with scalar subqueries to return a boolean true or false depending on whether the SELECT statement would return a row or not.

SQlALchemy provides the `exists()` method to generate an EXISTS subquery.

For example, the following query return `user_account`rows that have more than one related row in `address`:

```python
subq = (
    select(func.count(address_table.c.id))
    .where(user_table.c.id == address_table.c.user_id)
    .group_by(address_table.c.user_id)
    .having(func.count(address_table.c.id) > 1)
).exists()

stmt = (
    select(user_table.c.name)
    .where(subq)
)
```

Many times, EXIST queries are used as a negation, that is, as in NOT EXISTS.

The following example illustrates how to do that in SQLAlchemy code. The code retrieves all the users that don't have an email:

| NOTE: |
| :---- |
| The `~` operator is the equivalent of the SQL NOT condition. |

```python
subq = (
    select(address_table.c.id)
    .where(user_table.c.id == address_table.c.user_id)
).exists()

stmt = (
    select(user_table.c.name)
    .where(~subq)
)
```

#### Working with SQL functions

SQL functions are reusable expressions that process data and return a single result. They can be used for calculations, aggregations, or data transformations.

The `func` object serves as a factory for creating new `Function` objects, which when used in constructs like `select()`, produce a SQL function display, typically consisting of a name, some parenthesis, and possible some arguments.

Examples, of a few common functions are:

+ `func.count()`: aggregate function which counts how many rows are returned.

    ```python
    stmt = select(func.count()).select_from(user_table)
    ```

+ `func.lower()`: converts string to lowercase.

    ```python
    stmt = select(func.lower("Hello to Jason!"))
    ```

+ `func.now()`: provides the current date and time.

    ```python
    stmt = select(func.now())
    ```

Because most database backend provide their own set of functions, SQLAlchemy tries to be liberal as possible in what it accepts. Unfortunately, you will get an exception at runtime if a given DB does not support such function.

At the same time, SQLAlchemy provides a relatively small set of pre-packaged versions of the most common function with proper typing information to mitigate that risk.

You can inspect the return type of a function using:

```python
print(func.now().type) # DateTime
```

To apply a specific type to a function you're creating, use the `type_` parameter:

```python
from sqlalchemy import JSON

function_expr = func.json_object(
    '{a, 1, b, "def", c, 3.5}',
    type_=JSON
)
```

For common aggregate functions like `count()`, `max()`, `min()`, as well as for a very small number of date functions like `now()` and some string functions like `concat()`, the SQL return type is set appropriately based in usage and you don't need to do anything.

```python
func.concat("x", "y").type # String
```

##### Using window functions

A window function is a special use of a SQL aggregate function which calculates the aggregate value over the rows being returned in a group as the individual result rows are processed. The syntax include a SELECT statement with  an OVER (PARTITION BY ... ORDER BY ...) clause.

In SQL, window functions allow you to specify the rows over which the function should be applied, a "partition" value which considers the window over different subsets of rows, and an order by expression, which indicates the order in which rows should be applied to the aggregate function.

In SQLAlchemy, `over()` implements the `OVER (PARTITION BY ... ORDER BY ...)` syntax. As an example, the following snippet uses `row_number()` to (sort of) count each of the emails associated to each user:

```python
stmt = (
    select(
        func.row_number().over(partition_by=user_table.c.name),
        user_table.c.name,
        address_table.c.email_address
    )
    .select_from(user_table)
    .join(address_table)
)
```

In the following one, we use `over.order_by` to count the rows in each individual group identified by the name:

```python
stmt = (
    select(
        func.count().over(order_by=user_table.c.name),
        user_table.c.name,
        address_table.c.email_address,
    )
    .select_from(user_table)
    .join(address_table)
)
```

| NOTE: |
| :---- |
| The counter will increase with the different number of users and emails found. |

##### Special modifiers WITHIN GROUP, FILTER

WITHIN GROUP is used in conjunction with an "ordered set" or a "hypothetical set" aggregate function.

Common ordered set functions include `percentile_cont()` and `rank()`.

SQLAlchemy provides built-in implementations for `rank()`, `dense_rank()`, `mode()`, `percentile_cont()`, and `percentile_disc()`.

```python
print(
    func.unnest(
        func.percentile_disc([0.25, 0.5, 0.75, 1]).within_group(user_table.c.name)
    )
)
```

FILTER is supported by some backends to limit the range of an aggregate function to a particular subset of rows compared to the total range of rows returned, available using `filter()` method:

```python
stmt = (
    select(
        func.count(address_table.c.email_address).filter(user_table.c.name = "sandy"),
        func.count(address_table.c.email_address).filter(user_table.c.name == "spongebob"),
    )
    .select_from(user_table)
    .join(address_table)
)
```

##### Table-valued functions

Table-valued SQL functions support a scalar representation that contains named sub-elements. They're often used for JSON and ARRAY-oriente functions.

SQLAlchemy provides the `table_valued()` method as the basic table-valued function construct:

```python
onetwothree = func.json_each('["one", "two", "three"]').table_valued("value")
stmt = select(onetwothree).where(onetwothree.c.value.in_(["two", "three"]))
```

##### Column valued functions: table-valued functions as a scalar column

A special syntax is supported by Postgres and others to refer a function in the FROM clause which then delivers a single column in the columns clause of a SELECT statement or other column expression. This syntax is used for JSON related functions such as `json_object_keys()`, `json_each_text()`, `json_each()`, etc.

SQLAlchemy refers to this as a "column valued" function using `column_valued`:

```python
stmt = select(func.json_array_elements('["one", "two"]')).column_valued("x")
```

#### Data casts and type coercion

SQL supports CAST to tell the database the result of an otherwise ambiguous expression, or in some cases to convert the implied datatype into something else (e.g., `CAST(user_account.id as VARCHAR)`).

SQLAlchemy provides the `cast()` function for this purpose:

```python
from sqlalchemy import cast

stmt = select(cast(user_table.c.id, String))
with engine.connect() as conn:
    result = conn.execute(stmt)
```

Note that `cast()` will also produce the corresponding Python type as well:

```python
from sqlalchemy import JSON

print(cast("{'a': 'b'}", JSON)["a"])
```

##### `type_coerce()`: a Python-only cast

SQLAlchemy provides the `type_coerce()` function to let SQLAlchemy know the datatype of an expression without generating the corresponding SQL CAST expression.

```python
import json
from sqlalchemy import JSON, type_coerce

stmt = select(type_coerce({"some_key": {"foo": "bar"}}, JSON)["some_key"])
```

### Using UPDATE and DELETE statements

UPDATE and DELETE SQL statements are used to modify and delete existing rows.

#### Using UPDATE

The UPDATE SQL statement is used to modify existing rows.

The `update()` function generates a new instance of `Update` which represents the corresponding `UPDATE` statement in SQL.

The traditional form of UPDATE is performed against a single table at a time, and does not return any rows:

```python
from sqlalchemy import update

stmt = (
    update(user_table)
    .where(user_table.c.name == "patrick")
    .values(fullname="Patrick the Star")
)
```

The `values()` method controls the contents of the `SET` elements of the UPDATE statement. Parameters can be passed using the column names as keywords (as seen in the example above), and you can also use column expressions:

```python
stmt = (
    update(user_table)
    .where(user_table.c.name == "patrick")
    .values(fullname="Username: " + user_table.c.name)
)
```

To support an UPDATE in an "executemany" context, SQLAlchemy provides the `bindparam()` construct:

```python
from sqlalchemy import bindparam

stmt = (
    update(user_table)
    .where(user_table.c.name == bindparam("oldname"))
    .values(name=bindparam("newname"))
)

with engine.begin() as conn:
    conn.execute(
        stmt,
        [
            {"oldname": "jack", "newname": "ed"},
            {"oldname": "wendy", "newname": "mary"},
            {"oldname": "jim", "newname": "jake"},
        ]
    )
```

##### Correlated updates

An UPDATE can make use of rows in other tables by using a correlated subquery. A correlated subquery can be used anywhere a column expression might be used.

```python
scalar_subq = (
    select(address_table.c.email_address)
    .where(address_table.c.user_id == user_table.c.id)
    .order_by(address_table.c.id)
    .limit(1)
    .scalar_subquery()
)

update_stmt = update(user_table).values(fullname=scalar_subq)
```

##### UPDATE...FROM

Some DBs (e.g., Postgres) support the syntax UPDATE...FROM where additional tables may be stated directly in a special FROM clause.

This is implicitly generated by SQLAlchemy when additional tables are found in the `.where()` clause of an `update()`:

```python
update_stmt = (
    update(user_table)
    .where(user_table.c.id == address_table.c.id)
    .where(address_table.c.email_address == "patrick@example.com")
    .values(fullname="Pat")
)
```

UPDATE...FROM can also be combined with the `values()` construct to create a single `UPDATE` statement that updates multiple rows at once against the named form of VALUES:

```python
from sqlalchemy import Values

values = Value(
    user_table.c.id,
    user_table.c.name,
    name="my_values",
).data([(1, "new_name"), (2, "another_name"), ("3", "new_name")])

update_stmt = (
    user_table
    .update()
    .values(name=values.c.name)
    .where(user_table.c.id == values.c.id)
)
```

#### Using DELETE

The DELETE SQL statement is used to remove rows from a table.

SQLALchemy provides the `delete()` function.

```python
from sqlalchemy import delete

stmt = delete(user_table).where(user_table.c.name == "patrick")
```

Like `update()`, `delete()` supports the use of correlated subqueries in the `where()`:

```python
delete_stmt = (
    delete(user_table)
    .where(user_table.c.id == address_table.c.user_id)
    .where(address_table.c.email_address == "patrick@foo.com")
)
```

##### Getting affected row count from UPDATE, DELETE

Both `update()` and `delete()` support the ability to return the number of rows matched after the statement proceeds. This value will be available in the `Result.rowcount` property:

```python
with engine.begin() as conn:
    result = conn.execute(
        update(user_table)
        .values(fullname="Patrick McStart")
        .where(user_table.c.name == "patrick")
    )
    print(result.rowcount)
```

##### Using RETURNING with UPDATE, DELETE

Some backends support the RETURNING clause when issuing UPDATE or DELETE statements.

SQLAlchemy provides `Update.returning()` and `Delete.returning()` methods to model that functionality:

```python
update_stmt = (
    update(user_table)
    .where(user_table.c.name == "patrick")
    .values(fullname="Patrick the star")
    .returning(user_table.c.id, user_table.c.name)
)


delete_stmt = (
    delete(user_table)
    .where(user_table.c.name == "patrick")
    .returning(user_table.c.id, user_table.c.name)
)
```

## SQLAlchemy: ORM basics

### Working with DB metadata in ORM

When using ORM, the `MetaData` collection will be implicitly associated with an ORM-only construct called the **declarative base**.

The following snippet illustrates how to acquire a declarative base when using ORM:

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

### Declaring mapped classes

In the ORM API, `Table` objects are created declaratively using mapped classes.

The following snippet illustrates how to create a `User` and `Address` tables when using the ORM API:

```python
from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "user_account

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str | None]

    addresses: Mapped[list[Address]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))

    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
```

These are the details worth mentioning from the mapped classes above:

+ **Tables**: Each class inherits from `Base` which enables it to work with the underlying `MetaData` object. That's the case for `__tablename__` which sets the underlying table name the mapped class represents.
    + All the classes inheriting from `Base` will be given an initializer that will accept all attribute names as optional keyword arguments. You can override this `__init__()` method if required.
    + You can create extra methods in your mapped classes. In the example above, you can see the `__repr__()` methods for the dev-level representation of the objects.

+ **Column specification**: `mapped_column()` is used to indicate the columns in the `Table`, in conjunction with the typing annotations using the `Mapped` type.
    + Simpler columns (the ones that require just a datatype and no other options) can be specified with `Mapped` type annotation only.
    + A column can be declared "nullable" based on the `| None` specification.

+ **Relationships**: `User.addresses` and `Address.user` are two attributes of the mapped classes that do not derive any DDL definitions, but will help your Python programs.

### Using SELECT statements in ORM

The SQL SELECT statements are used to fetch rows from one or more DB tables.

When using the ORM API, you will have the same sort of composable API that is available in SQLAlchemy Core API, but with certain differences.

For example, to open a connection to the database, you will have to use a `Session` object (instead of using `Connection.connect()` or `Connection.begin()`). Also, the you will pass to `Select` and chained methods, the mapped classes and attributes:

```python
stmt = (
    select(User)  # User is the mapped class
    .where(User.name == "spongebob") # User.name is the mapped class attribute
)

with Session(engine) as session:
    for row in session.execute(stmt):
        print(row)  # row is a tuple whose first element is a `User`
```

Also, like its counterpart, the `Session` features *commit as you go* behavior, so you'll need to invoke `Session.commit()` when altering data.

The following example uses a `Session` object to update a table using SQL:

```python
with Session(engine) as session:
    result = session.execute(
        text("UPDATE some_table SET y = :y where x = :x"),
        [{"x": 9, "y": 81}, {"x": 10, "y": 100}]
    )
    session.commit()
```

#### Getting the first result with `first()` and `ScalarResult`

You already know about `Result.first()` method which returns the first result from the retrieved rows.

```python
with Session(engine) as session:
    row = session.execute(select(User)).first()
```

Note that in the ORM case, `Row` is a tuple (as the result may contain multiple entities). Thus, you'll need to use `row[0]` to get the corresponding `User` instance from the `Result`.

Alternatively, to avoid doing `row[0]` you can use `Session.scalars()`:

```python
with Session(engine) as session:
    user = session.scalars(select(User)).first()
```

Note that `Session.scalars()` execute the statement directly, so you won't need to invoke `Session.execute(stmt)`. The method will deliver the first element of each row, which in this case will be a `User` instance.

#### Getting all the results with `all()`

You can also use `Result.all()` to materialize all the results when using the ORM API:

```python
with Session(engine) as session:
    rows = session.execute(select(User)).all()
```

#### Combining multiple entities

When using the ORM API, you can combine multiple entities in your SELECTs:

```python
with Session(engine) as session:
    rows = session.execute(
        select(User.name, Address)
        .where(User.id == Address.user_id)
        .order_by(Address.id)
    )
```

#### ORDER BY in ORM

In the ORM API, the ORDER BY clause is used in the same way as in the Core API:

```python
stmt = (
    select(User)
    .order_by(User.fullname.desc)
)
```

#### Aggregate functions in ORM

The following snippet illustrates how to write SELECT queries with aggregate functions and GROUP BY / HAVING.

```python
with Session(engine) as session:
    result = session.execute(
        select(User.name, func.count(Address.id).label("count"))
        .join(Address)
        .group_by(User.name)
        .having(func.count(Address.id) > 1)
    )
```

#### ORM entity aliases

The syntax for using entity aliases when using the ORM API is the following:

```python
from sqlalchemy.orm import aliased

address_alias_1 = aliased(Address)
address_alias_2 = aliased(Address)

stmt = (
    select(User)
    .join_from(User, address_alias_1)
    .where(address_alias_1.email_address == "patrick@aol.com")
    .join_from(User, address_alias_2)
    .where(address_alias_2.email_address == "patrick@example.com")
)
```

#### ORM entity subqueries

The following snippet illustrates how to work with subqueries in the ORM API:

```python
subq = (
    select(Address)
    .where(~Address.email_address.like("%@aol.com"))
    .subquery()
)

address_subq = aliased(Address, subq)

stmt = (
    select(User, address_subq)
    .join_from(User, address_subq)
    .order_by(User.id, address_subq.id)
)

with Session(engine) as session:
    for user, address in session.execute(stmt):
        print(f"{user} {address}")
```

| NOTE: |
| :---- |
| The `~` operator is the equivalent of the SQL NOT condition. |


#### ORM CTEs

When using the ORM APIs, CTEs are expressed as follows:

```python
cte_obj = (
    select(Address)
    .where(~Address.email_address.like("%@aol.com"))
    .cte()
)

address_cte = aliased(Address, cte_obj)

stmt = (
    select(User, address_cte)
    .join_from(User, address_cte)
    .order_by(User.id, address_cte.id)
)

with Session(engine) as session:
    for user, address in session.execute(stmt):
        print(f"{user} {address}")
```

| NOTE: |
| :---- |
| The `~` operator is the equivalent of the SQL NOT condition. |

#### Selecting ORM entities from unions

When using ORM, unions are perfomed as follows:

```python
stmt1 = select(User).where(User.name == "sandy")
stmt1 = select(User).where(User.name == "spongebob")
u = union_all(stmt1, stmt2)
```

For simple SELECT with UNION that is not already nested inside a subquery, these can be often be used in an ORM object fetching context by using the `Select.from_statement()` method. With this approach, the UNION statement represents the entire query:

```python
orm_stmt = select(User).from_statement(u)

with Session(engine) as session:
    for obj in session.execute(orm_stmt).scalars():
        print(obj)
```

To use a UNION or other set-related construct as an entity related component in a more flexible manner:

```python
user_alias = aliased(User, u.subquery())
orm_stmt = select(user_alias).order_by(user_alias.id)

with Session(engine) as session:
    for obj in session.execute(orm_stmt).scalars():
        print(obj)
```

### Inserting rows using the ORM Unit of Work pattern

When using the ORM API, the `Session` object is responsible for constructing `Insert` constructs and emitting them as INSERT statements within the ongoing transaction.

You do that by adding objects to the `Session`, which in turn, makes sure these new entries will be emitted to the DB when they are needed, using a process known as a *flush*.

The overall process used by the `Session` to persist objects is known as the **Unit of Work** pattern.

#### Creating objects representing rows

You will typically start by creating regular Python objects from your mapped classes. Those represent potential database rows to be inserted:

```python
squidward = User(name="squidward", fullname="Squidward Tentacles")
krabs = User(name="mrkrabs", fullname="Eugene H. Krabs")
```

Note that you don't need to include the value for the primary key (i.e., an entry for the `id` column), since you would like to make use of the auto-incrementing primary key feature of the DB.

That is, then creating the object, the value of the `id` field will be `None`.

At this point, both objects that have been created but haven't been yet associated with a `Session` object, are called to be in a state called **transient**.

#### Adding objects to a `Session`

In the next step, you should create a `Session` (typically using a context manager, but you can also doing without it provided that you close the session explicitly), and add the objects to the `Session` using the `add()` method.

This will change the state of the objects from transient to **pending**:

```python
with Session(engine) as session:
    session.add(squidward)
    session.add(krabs)
```

You can see the pending objects managed by a session object using `Session.new` attribute:

```python
print(session.new)
# IdentitySet(
#     [
#         User(id=None, name='squidwar'), ...),
#         User(id=None, name='mrkrabs', ...)
#     ]
# )
```

| NOTE: |
| :---- |
| An `IdentitySet` is a Python set that hashes on an object identity, rather than using the `hash()` function. |


#### Flushing

The `Session` is used to accumulate changes one at a time using the `add()` method, but it does not communicate those changes to the DB until needed.

This allows for optimizing the way in which the SQL DML statements should be emitted in the transaction based on a given set of pending changes.

The process in which all the changes maintained by the `Session` are sent to the DB is known as a **flush**.

The ORM API provides a `Session.flush()` method you can use for this purpose, although it is usually unnecessary and the `Session` knows how to flush changes when needed (using a behavior known as *autoflush*), and in any case, a **flush** will automatically happen when `Session.commit()` is called.

In any case, when calling `Session.flush()`, a new transaction will be created and the necessary DML statements will be emitted to the DB.

The transaction will remain open until `Session.commit()`, `Session.rollback()`, or `Session.close()` are called.

Once the objects have been sent to the DB, the objects will be in the **persistent state**.

In the case of the example illustrated above, in which we were inserting two objects, you will see that the Python objects will then have primary key identifiers:

```python
print(squidward.id) # 4
print(krabs.id) # 5
```

#### Getting objects by primary key from the identity map

The objects are now linked to the `Session` object by way of the primary key identity in a memory structure known as the identity map.

Th identity map is an in-memory story that links all objects currently loaded in memory, keyed by their primary key.

The method `Session.get()` lets you get a reference to an object in this identity map:

```python
some_squidward = session.get(User, 4)

print(some_squidward is squidward) # True
```

Note that the identity map maintains a unique instance of particular Python object with the scope of a particular `Session` object.

#### Committing

Once you're done with all the necessary object manipulations, you just need to invoke `Session.commit()` to close the transaction:

```python
session.commit()
```

After a `commit()`, the persistent object will be still attached to the `Session` object, and will remain so until the `Session` is closed.

| NOTE: |
| :---- |
| Attributes on the objects committed will have expired after a `commit()`, meaning that when we next access any attributes on them, the `Session` will start a new transaction and re-load their state, which might not be desirable in some situations. |

### Updating ORM objects using the Unit of Work pattern

Let's assume that we load a `User` object into the session, which will automatically open a transaction:

```python
sandy = session.execute(
    select(User)
    .filter_by(name="sandy")
).scalar_one()
```

The `Result.scalar_one()` method returns exactly one scalar, that is, one value representing an object, or raises an exception.

The retrieved Python object acts as a proxy for the row in the DB, but it is primarily a Python object we can work with:

```python
sandy.fullname = "Sandy Cheeks the Squirrel"
```

Once we alter the object, the `Session` will make note that the object has some modifications pending by placing a reference to that object in the `dirty` collection:

```python
print(sandy in session.dirty) # True
```

When the `Session` next emits a flush, the corresponding UPDATE will be emitted automatically to update this value in the DB. In particular, a flush will occur automatically before we emit any SELECT (because of the autoflush behavior).

That is, whenever you do:

```python
sandy_fullname = session.execute(
    select(User.fullname)
    .where(User.id == 2)
).scalar_one()

print(sandy_fullname) # Sandy Cheeks the Squirrel
print(sandy in session.dirty) # False
```

Note that after having flushed the updates to the DB, the object will no longer be in the `session.dirty` collection.

This does not mean that the changes have been effectively committed in the DB. At this point, the transaction is still open.

### Deleting ORM objects using the Unit of Work pattern

An individual ORM object may be marked for deletion within the unit of work by using the ``Session.delete()` method.

```python
patrick = session.get(User, 3)

session.delete(patrick)
```

As with other ORM operations, nothing will actually happen until a flush is carried out.

You can force an autoflush by issuing a SELECT:

```python
session.execute(
    select(User)
    .where(User.name == "patrick")
    .first()
)
```

If you look at the logs you'll see that the SELECT would be preceded by a DELETE.

At this point, the `patrick` object will no longer be in the `Session`:

```python
print(patrick in session) # False
```

# Bulk / Multirow INSERT, upsert, UPDATE and DELETE

The ORM session has the ability to process commands that allow to emit INSERT, UPDATE, and DELETE statements directly without being passed any ORM-persisted objects, by receiving instead list of values to be inserted, updated, upserted, or value for WHERE so that an UPDATE or DELETE matching many rows can be invoked.

This mode is particularly useful when large number of rows must be modified without needed to construct and manipulate mapped objects, which may be cumberson in such cases.

The bulk/multirow features of the `Session` make use of the `insert()`, `update()`, and `delete()` constructs directly, and their usage resembles how they are used in the Core API.

For example, you can do:

```python
from sqlalchemy import insert

session.execute(
    insert(User),
    [
        {"name": "spongebob", "fullname": "Spongebob Squarepants"},
        {"name": "sandy": "fullname": "Sandy Cheeks"},
        {"name": "patrick", "fullname": "Patrick Star"},
    ]
)
```

### Rolling back

The `Session.rollback()` method emits a ROLLBACK on the underlying SQL transaction in progress.

Using `rollback()` will not only rollback the transaction, but will also expire all the objects that were associated with the `Session`, which will then have to be refreshed when next accessed.

The process is illustrated in the following snippet:

```python
session.rollback()

print(sandy.__dict__) # no state on sandy (expired)

print(sandy.fullname) # this will triger a SELECT to refresh

print(patrick in session) # True

some_patrick = session.execute(
    select(User)
    .where(User.name == "patrick")
).scalar_one()

print(some_patrick is patrick) # True
```

As you can see, for delete objects (`patrick`), the object identity will be restored and will still be present in the database

### Closing a session

A `Session` will be automatically closed when using the `Session` object within a *context manager*.

The following happens when a session is closed:
+ All connections to the connection pool are released, rolling back any transactions that were in progress.

    As a consequence, there's no need to explicitly call `Session.rollback()` to make sure transaction is rolled back.

+ All objects from the `Session` are expunged.

    All Python objects that had been added to the `Session` will transition to a *detached* state. If you try to use an object in such state you'll get a `DetachedInstanceError`.

    Detached objects can be reassociated using the `Session.add()` method.

| NOTE: |
| :---- |
| You should avoid using objects in their detached state. If possible, you should clean up all references to all the previously attached objects when the session is closed. |

### Working with relationships

In the section in which [mapped classes were introduced](#declaring-mapped-classes), you saw that the classes made use of a construct called `relationship()`.

This construct defines a linkage between two different mapped classes, or from a mapped class to itself.

Let's focus on the relationship part of our mapped classes:

```python
from __future__ import annotations

from sqlalchemy.orm import Mapped, relationship

class User(Base):
    __tablename__ = "user_account"

    # ... mapped_column() mappings ...

    addresses: Mapped[List[Address]] = relationship(back_populates="user")

class Address(Base):
    __tablename__ = "address"

    # ... mapped_column() mappings ...

    user: Mapped[User] = relationship(back_populates="addresses")
```

The `User` class has an attribute `addresses`, and the `Address` class has an attribute `user`.

The `relationship()` construct, along with the `Mapped` typing, is used by SQLAlchemy to inspect the table relationships between the `Table` objects.

As the `address` table has a foreign key constraint which refers to the `user_account` table, the relationship can determine unambigously that there is a *one-to-many* relationshop from the `User` class to the `Address` class: one particular row in the `user_account` may be referenced by many rows in the `address` table.

All one-to-many relationships naturally correspond to a many-to-one relationship in the other direction, as see by the `Address.user` property.

The `back_populates=...` parameter established that each of these two relationship constructs should be considered complimentary to each other.

#### Persisting and loading relationships

If you make a new `User` object, you will see that addresses is a Python list:

```python
u1 = Username(name="pearl", fullname="Pearl Krabs")
print(u1.addresses) # []
```

At that point, the `u1` object is still transient, and the `u1.addresses` list has not been mutated. While the list is a special SQLAlchemy-specific version of a Python list that can track and respond to changes made to it, you can work with it as if it were a regular Python list:

```python
a1 = Address(email_address="pearl@example.com")
u1.addresses.append(a1)
print(u1.addresses) # Address(id=None, email_address="pearl@example.com")
```

The interesting point is that the counterpart `a1.user` will have been updated automatically:

```python
print(a1.user) # User(id=None, name="pearl", fullname="Pearl Krabs")
```

This synchronization happened thanks to the `backpopulates=...` parameter of the `relationship()` declaration. And it will work on the other direction too:

```python
a2 = Address(email_address="pearl@foo.com", user=u1)
print(u1.addresses)
# [
#   Address(id=None, email_address="pearl@example.com"),
#   Address(id=None, email_address="pearl@foo.com"),
#]
```

Note that at this point, the objects are still transient as they hadn't been associated to any `Session` object yet.

#### Cascading objects into the session

Let's now make those objects **pending** (make them transition from *transient* to *pending*) by adding them into the session, starting with the `User` object `u1`:

```python
session.add(u1)
```

If we now interrogate the `session` we will see:

```python
print(u1 in session) # True

print(a1 in session) # True
print(a2 in session) # True
```

As you see, because of the `relationship()` specification, adding `u1` to the session caused the automatic addition of the `Address` objects into the session as well, in a process known as *save-update cascade*.

The objects are still in *pending* state and they haven't been persisted into the DB, and their corresponding `id` fields will be `None`.

When a `Session.commit()` is used, SQLAlchemy will automatically generate the necessary INSERT, UPDATE, and DELETE statements and in the correct order (e.g., in the situation above, `User` should be persisted before `Address` instances).

#### Loading relationships

By default, calling `Session.commit()` expires all objects in the session, so that they refresh for the next transaction.

These means that as soon as you access an attribute on any of these objects, you'll see SELECT statements emitted to load the objects into the session again.

This will affect all primary attributes of the object. That is, in the particular case of the `User` object, the `id`, `name` and `fullname` will be retrieved, but not the `User.addresses`.

However, as soon as you access `addresses`, another SELECT statement will be issued. This is known as *lazy loading*, and that's the default behavior for relationships.

Once relationships are available in memory, no SQL will be emitted until that collection or attribute mentioned in the relationship is expired. You can add or remove items from `addresses` and you won't see any SQL calls.

However, you should be aware of this lazy loading behavior, as it may become expensive very quickly, if you don't take the necessary steps to optimize it.

#### Using relationships in JOINs

When using ORM entities, you can rely on the relationship declared on a mapped class to set up the ON clause of a JOIN.

The attribute associated to the `relationship()` specification may be passed as a single argument to `join()` to specify in one shot both the right-hand side of the JOIN, and the ON clause:

```python
# SELECT address.email_address
#   FROM user_account
#   JOIN address
#     ON user_account.id = address.user_id
stmt = (
    select(Address.email_address)
    .select_from(User)
    .join(User.addresses)
)
```

#### Loader strategies

You've seen that by default, the attributes that are mapped using `relationship()` will emit a lazy load when the collection is not populated but it's needed.

Lazy loading is one of the most controversial operations, because having dozen objects in memory with relationships can trigger many additional queries. This is known as the N plus one problem.

Apart from the performance problems, those additional queries that are triggered implicitly, may cause problems if there's no running DB transaction available, or when using asyncio.

It is recommended that you test the application with SQL echo on, and review the SQL that is emitted. If the lazy loading works for you, you should keep *lazy loading* as the default strategy.

On the other hand, if you see lots of redundant SELECTs, or happening for objects that have been detached from their `Session` and therefore causing additional performance problems, you should look into alternative *loader strategies*.

Loader strategies are represented as objects that may be associated with a SELECT statement using `Select.options()` method:

```python
for user_obj in session.execute(
    select(User).options(selectinload(User.addresses)).scalars()
):
    print(user_obj.addresses) # preloaded!
```

In the snippet above, you are pre-loading `User.addresses` so that no implicit query is triggered when addresses are accessed for the first time.

The strategy can also be configured in the `relationship()` specification:

```python
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user_account"

    addresses: Mapped[List[Address]] = relationship(back_populates="user", lazy="selectin")
```

##### Selectin load

The `selectinload()` loader strategy solves the most common form of the *N plus one* problem which is that of a set of objects that refer to related collections.

`selectinload()` will ensure that a particular collection for a full series of objects are loaded up front using a single query. It does this using a SELECT form that in most cases can be emitted agains the related table alone, without introducing JOINs or subqueries, and only queries for those parent objects for which the collection is already loaded.

The following snippet loads all the `User` objects and their related `Address` objects using this strategy.

```python
from sqlalchemy.orm import selectinload

stmt = (
    select(User)
    .options(selectinload(User.addresses))
    .order_by(User.id)
)

for row in session.execute(stmt):
    emails = ', '.join(a.email_address) for a in row.User.addresses
    print(
        f"{row.User.name} ({emails})")
```

##### Joined load

The `joinedload()` strategy augments the SELECT statement that is passed to the database with a JOIN (which may be outer or inner join, depending on the options), which can then load in related objects.

This strategy is appropriate to load many-to-one objects, as it only requires that additional columns are added to a primary entity row that would be fetched in any case.

For greated efficiency, it also accepts an option `joinedload.innerjoin` so that an inner join is used instead of an outer join in cases in which you are not interested in getting nulls when the joined columns don't match.

The case below illustrates this approach, in which we load all `Address` object for a `User`, where INNER JOIN can be used as all `Address` objects have a `User`:

```python
from sqlalchemy.orm import joinedload

stmt = (
    select(Address)
    .options(joinedload(Address.user, innerjoin=True))
    .order_by(Address.id)
)
for row in session.execute(stmt):
    print(f"{row.Address.email_address} {row.Address.user.name}")
```


While `joinedload()` also works for collections (i.e., one-to-many relationships), it has the effect of multiplying out primary rows per related item in a recursive way that grows the amount of data sent for a result set by orders or magnitude for nested collections and/or larger collections-

##### Explicit join + eager load

If you were you load `Address` rows while joining to the `user_account` table using a method such as `Select.join()`, you could easily leverage that JOIN in order to eagerly load the contents of the `Address.user` attribute on each of the `Address` objects returned.

That is essentially, the `contains_eager()` option, which is very similar to `joined_load()`, except that it assumes that you have set up the JOIN yourself, and therefore, only indicates that additional columns will have to be fetched:


```python
from sqlalchemy.orm import contains_eager

stmt = (
    select(Address)
    .join(Address.user)
    .where(User.name == "pearl")
    .options(contains_eager(Address.user))
    .order_by(Address.id)
)

for row in session.execute(stmt):
    print(f"{row.Address.email_address} {row.Address.user.name}")
```

##### Raise load

The `raiseload()` option is used to completely block your app from having the N plus one problem by raising an error instead of issuing the default lazy load.

It has two variants controlled with the `sql_only` parameter to block lazy loads that require SQL, vs. all load operations, including those that don't require SQL and simply consult the current `Session`.

The following snippet configures the `relationship()` to use this strategy:

```python
from __future__ import annotations

from sqlalchemy.orm import Mapped, relationship

class User(Base):
    __tablename__ = "user_account"

    # ... mapped_column() mappings ...

    addresses: Mapped[List[Address]] = relationship(back_populates="user", lazy="raise_on_sql")

class Address(Base):
    __tablename__ = "address"

    # ... mapped_column() mappings ...

    user: Mapped[User] = relationship(back_populates="addresses", lazy="raise_on_sql")


u1 = session.execute(select(User)).scalars().first() # OK
print(u1.addresses) # Raises InvalidRequestError
```

In order to prevent the exception from raising, you'd just need to load the relationship up front using any other strategy:

```python
u1 = (
    session.execute(
        select(User)
        .options(selectinload(User.addresses))
    ).scalars().first()
)

print(u1.addresses) # OK, as it was preloaded
```

## Asyncio integration

### Async Core API

For SQLAlchemy Core API, the `create_async_engine()` function creates an instance of `AsyncEngine`, which then offers an async version of the `Engine` API.

In turn, `AsyncEngine` returns an `AsyncConnection` using `AsyncEngine.connect()` and `AsyncEngine.begine()` which can be used using *async context manager protocol*.

With an AsyncConnection, you can invoke `AsyncConnection.execute()` to deliver a buffered `Result`, or `AsyncConnection.stream()` to deliver a streaming `AsyncResult`.

The following snippet illustrates how to work with `asyncio` and SQLAlchemy's Core API:

```python
from sqlalchemy.ext.asyncio import create_async_engine

meta = MetaData()

t1 = Table("t1", meta, Column("name", String(50), primary_key=True))

async def async_main() -> None:
    engine = create_async_engine("sqlite+aiosqlite://", echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)

        await conn.execute(
            insert(t1),
            [
                {"name": "some name 1"},
                {"name": "some name 2"},
            ]
        )

    async with engine.connect() as conn:
        result = await conn.execute(select(t1).where(t1.c.name == "some name 1"))

        print(result.all())

    # Release the engine defined at the function scope
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(async_main())
```

+ `AsyncConnection.run_sync()` is the proper way to invoke functions that generate DDL that don't include an awaitable hook.

+ It's recommended to await the invocation of `AsyncEngine.dispose()` when the `AsyncEngine` object in scope will go out of context. That will ensure that any connections held by the connection pool will be properly released. This is your responsibility, as SQLAlchemy won't be able to invoke it for you.

The following snippet inllustrates how to work with the Streaming API:

```python
async with engine.connect() as conn:
    async_result = await conn.stream(select(t1))

    async for row in async_result:
        print(f"{row=}")
```

### Async ORM

In ORM, the `AsyncSession` provides full ORM functionality.

Within the default mode, you should pay special attention to avoid lazy loading or expired-attribute access involving ORM relationships and column attributes.

Additionally, a single instance of `AsyncSession` is not safe for use in multiple concurrent tasks.

The following snippet illustrates a complete example of SQLAlchemy Async ORM API, including mapper and session configuration.

```python
...
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    AsyncSession
)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class B(Base):
    __tablename__ = "b"

    id: Mapped[int] = mapped_column(primary_key=True)
    a_id: Mapped[int] = mapped_column(ForeignKey("a.id"))
    data: Mapped[str]

class A(Base):
    __tablename__ = "a"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[str]
    create_date: Mapped[datetime] = mapped_column(server_default=func.now())
    bs: Mapped[List[B]] = relationship()

async def insert_objects(async_session: async_sessionmaker[AsyncSession]) -> None:
    async with async_session() as session:
        async with session.begin():
            session.add_all([
                A(bs=[B(data="b1"), B(data="b2")], data="a1"),
                A(bs=[], data="a2"),
                A(bs=[B(data="b3"), B(data="b4")], data="a3"),
            ])

async def select_and_update_objects(async_session: async_sessionmaker[AsyncSession]) -> None:
    async with async_session as session:
        stmt = (
            select(A)
            .order_by(A.id)
            .options(selectinload(A.bs))
        )
        result = await session.execute(stmt)

        for a in result.scalars():
            print(f"{a=}, {a.data=}")
            print(f"created at: {a.create_date}")
            for b in a.bs:
                print(f"{b=}, {b.data=})

        result = await session.execute(
            select(A)
            .order_by(A.id)
            .limit(1)
        )

        a1 = result.scalars().one()

        a1.data = "new data"
        await session.commit()

        # access attribute after commit
        print(f"{a1.data=}")

        # using AsyncAttrs to access an attribute as an awaitable
        for b1 in await a1.awaitable_attrs.bs:
            print(b1, b1.data)

    async def async_main() -> None:
        engine = create_async_engine("sqlite+aiosqlite://", echo=True)

        # async_sessionmaker is a factory for new AsyncSession objects.
        # expire_on_commit is set to False so that you can access
        # objects after transaction is committed.
        async_session = async_sessionmaker(engine, expire_on_commit=False)

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        await insert_objects(async_session)
        await select_and_update_object(async_session)

        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(async_main())
```

#### Using AsyncSession with concurrent tasks

The `AsyncSession` object is a mutable stateful object, which represents a single, stateful database transaction in progress.

This means that when you are using concurrent tasks with asyncio (.e.g, `asyncio.gather()`, `TaskGroup`, etc.) you must use a separate `AsyncSession` per individual task.

#### Preventing implicit I/O when using `AsyncSession`

When using async ORM, you must pay special attention to avoid any points at which I/O on attribute access may occur.

There are several techniquest to work around that:

+ Attributes that are lazy-loading relationships, deferred columns or expressesion, or are being accessed in expiration scenarios can take advantage of the `AsyncAttrs` mixin. This mixin provides an accessor `AsyncAttrs.awaitable_attrs` that delivers any attribute as an awaitable:

    ```python
    class Base(AsyncAttrs, DeclarativeBase):
        pass

    class A(Base):
        __tablename__ = "a"
        # ... other mappings ...
        bs: Mapped[List[B]] = relationship()

    class B(Base):
        __tablename__ = "b"
        # ... other mappings ...
    ```

    Accessing `A.bs` collection on newly loaded instances of A will use lazy loading by default, which will emit I/O to the DB. In order to access that attribute you can use the `AsyncAttrs.awaitable_attrs` prefix:

    ```python
    a1 = (await session.scalars(select(A))).one()
    for b1 in await a1.awaitable_attrs.bs:
        print(b1)
    ```

+ Collections can be replaced with write only collections that will never emit I/O implicitly, by using the write only relationships features in SQLAlchemy 2.0.

    ```python
    # ... other imports ...
    from sqlalchemy.orm import WriteOnlyMapped


    class Base(AsyncAttrs, DeclarativeBase):
        pass


    class A(Base):
        __tablename__ = "a"

        id: Mapped[int] = mapped_column(primary_key=True)
        data: Mapped[Optional[str]]
        create_date: Mapped[datetime.datetime] = mapped_column(
            server_default=func.now()
        )

        # collection relationships are declared with WriteOnlyMapped.
        bs: WriteOnlyMapped[B] = relationship()


    class B(Base):
        __tablename__ = "b"

        id: Mapped[int] = mapped_column(primary_key=True)
        a_id: Mapped[int] = mapped_column(ForeignKey("a.id"))
        data: Mapped[Optional[str]]


    async def async_main():
        """Main program function."""

        engine = create_async_engine(
            "postgresql+aiosqlite://", echo=True)

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async_session = async_sessionmaker(engine, expire_on_commit=False)

        async with async_session() as session:
            async with session.begin():
                # WriteOnlyMapped may be populated using any iterable,
                # e.g. lists, sets, etc.
                session.add_all(
                    [
                        A(bs=[B(), B()], data="a1"),
                        A(bs=[B()], data="a2"),
                        A(bs=[B(), B()], data="a3"),
                    ]
                )

            stmt = select(A)

            result = await session.scalars(stmt)

            for a1 in result:
                print(a1)
                print(f"created at: {a1.create_date}")

                # to iterate a collection, emit a SELECT statement
                for b1 in await session.scalars(a1.bs.select()):
                    print(b1)

            result = await session.stream(stmt)

            async for a1 in result.scalars():
                print(a1)

                # similar using "streaming" (server side cursors)
                async for b1 in (await session.stream(a1.bs.select())).scalars():
                    print(b1)

            await session.commit()
            result = await session.scalars(select(A).order_by(A.id))

            a1 = result.first()

            a1.data = "new data"


    asyncio.run(async_main())
    ```

    When using write-only collections, the program's behavior is simple and easy to predict regarding collections. However, the downside is that there's no built-in system for loading many of these collections all at once, which instead would need to be performed manually.

+ If not using `AsyncAttrs`, relationships can be declared with `lazy=raise` to that you get an exception when implicit I/O would be triggered.

+ You can rely on `selectinload()`, to eagerly load the collections.

## Alembic

Alembic is a tool for the creation, management, and invocation of *migrations* for a relational DB, using SQLAlchemy as the underlying engine.

You will typically install Alembic within your local virtual environment using as a development dependency.

```bash
uv add --dev alembic
```

### The migration environment

Usage of Alembic starts with the creation of the *Migration environment*. This is a directory of scripts that is specific to a particular application.

This migration environment is created just once, and is then maintained along with the application's source code itself.

The environment is created using the `init` command, and it looks like the following

```
009_sqlalchemy_alembic_hello/
├── README.md
├── main.py
├── pyproject.toml
└── uv.lock
```

```bash
# Create a migration environment using `alembic/` as the dir name
$ uv run alembic init alembic
  Creating directory /home/.../009_sqlalchemy_alembic_hello/alembic ...  done
  Creating directory /home/.../009_sqlalchemy_alembic_hello/009_sqlalchemy_alembic_hello/alembic/versions ...  done
  Generating /home/.../009_sqlalchemy_alembic_hello/009_sqlalchemy_alembic_hello/alembic/env.py ...  done
  Generating /home/.../009_sqlalchemy_alembic_hello/009_sqlalchemy_alembic_hello/alembic.ini ...  done
  Generating /home/.../009_sqlalchemy_alembic_hello/009_sqlalchemy_alembic_hello/alembic/script.py.mako ...  done
  Generating /home/.../009_sqlalchemy_alembic_hello/009_sqlalchemy_alembic_hello/alembic/README ...  done
  Please edit configuration/connection/logging settings in /home/.../009_sqlalchemy_alembic_hello/009_sqlalchemy_alembic_hello/alembic.ini before proceeding.
```

After running the command you will notice the following directories and files created:


```
../009_sqlalchemy_alembic_hello/
├── README.md
├── alembic/           # home dir for migration environment
│   ├── README         # information about migrations
│   ├── env.py         # customizable script invoked in migrations
│   ├── script.py.mako # template to generate migrations in versions/
│   └── versions/      # where migrations will be stored
├── alembic.ini        # main config file
├── main.py
├── pyproject.toml
└── uv.lock
```

+ `alembic.ini`: Alembic's main configuration file. Note that the information in this file can also be included in your `pyproject.toml`.

+ `alembic/`: Home directory of your migration environment. This is using the default name, but the name can be changed. A project with multiple DBs may have more than one of these directories.

+ `alembic/env.py`: Python script that is run whenever the Alembic migration tool is invoked.

    At the very least contains the instructions to configure and generate a SQLAlchemy engine, procure a connection from that engine along with a transaction, and then invoke the migration engine providing that connection.

    The script can be modified if required to include custom arguments to be made available to the migration environment, use app-specific libraries, etc.

+ `alembic/README`: README file for migrations that should include information for the end-user. By default, it contains a one-liner explaining this is the generic config for a single DB project.

+ `script.py.mako`: A [Mako](https://github.com/sqlalchemy/mako) template file which is used to generate new migration scripts.

    The template will be used to generate new files within `versions/`. This is also customizable, so that you can update the structure of `upgrade()` and `downgrade()`.

+ `versions/`: Directory holding the individual version scripts. Files here will be named using a partial GUID approach such as:

    ```
    versions/
        3512b954651e_add_account.py
        2b1ae634e5cd_add_order_id.py
        3adcc9a56557_rename_username_field.py
    ```

#### Editing the `.ini` file

Alembic will look into the current directory for an `alembic.ini` file.

The initial `.ini` file generated by the default template looks like the this:

```ini
# A generic, single database configuration.

[alembic]
# path to migration scripts.
# this is typically a path given in POSIX (e.g. forward slashes)
# format, relative to the token %(here)s which refers to the location of this
# ini file
script_location = %(here)s/alembic

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# see https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file
# for all available tokens
# file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s
# Or organize into date-based subdirectories (requires recursive_version_locations = true)
# file_template = %%(year)d/%%(month).2d/%%(day).2d_%%(hour).2d%%(minute).2d_%%(second).2d_%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.  for multiple paths, the path separator
# is defined by "path_separator" below.
prepend_sys_path = .


# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the tzdata library which can be installed by adding
# `alembic[tz]` to the pip requirements.
# string value is passed to ZoneInfo()
# leave blank for localtime
# timezone =

# max length of characters to apply to the "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version location specification; This defaults
# to <script_location>/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path.
# The path separator used here should be the separator specified by "path_separator"
# below.
# version_locations = %(here)s/bar:%(here)s/bat:%(here)s/alembic/versions

# path_separator; This indicates what character is used to split lists of file
# paths, including version_locations and prepend_sys_path within configparser
# files such as alembic.ini.
# The default rendered in new alembic.ini files is "os", which uses os.pathsep
# to provide os-dependent path splitting.
#
# Note that in order to support legacy alembic.ini files, this default does NOT
# take place if path_separator is not present in alembic.ini.  If this
# option is omitted entirely, fallback logic is as follows:
#
# 1. Parsing of the version_locations option falls back to using the legacy
#    "version_path_separator" key, which if absent then falls back to the legacy
#    behavior of splitting on spaces and/or commas.
# 2. Parsing of the prepend_sys_path option falls back to the legacy
#    behavior of splitting on spaces, commas, or colons.
#
# Valid values for path_separator are:
#
# path_separator = :
# path_separator = ;
# path_separator = space
# path_separator = newline
#
# Use os.pathsep. Default configuration used for new projects.
path_separator = os

# set to 'true' to search source files recursively
# in each "version_locations" directory
# new in Alembic version 1.10
# recursive_version_locations = false

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

# database URL.  This is consumed by the user-maintained env.py script only.
# other means of configuring database URLs may be customized within the env.py
# file.
sqlalchemy.url = driver://user:pass@localhost/dbname


[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# lint with attempts to fix using "ruff" - use the module runner, against the "ruff" module
# hooks = ruff
# ruff.type = module
# ruff.module = ruff
# ruff.options = check --fix REVISION_SCRIPT_FILENAME

# Alternatively, use the exec runner to execute a binary found on your PATH
# hooks = ruff
# ruff.type = exec
# ruff.executable = ruff
# ruff.options = check --fix REVISION_SCRIPT_FILENAME

# Logging configuration.  This is also consumed by the user-maintained
# env.py script only.
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```


| NOTE: |
| :---- |
| Alembic also includes other templates. This can be listed using `alembic list_templates` (e.g., there's a template to include the `.ini` information in your `pyproject.toml`). |


The following features are worth mentioning:

+ `[alembic]`: Indicates the section that will be read by Alembic to determine the configuration.

+ `alembic.script_location`: The location of the Alembic environment, as a filesystem location relative to `%(here)s` which indicates where the config file is located.

+ `alembic.file_template`: Specifies the naming schema used to generate new migration files. The default is `%%(rev)s_%%(slug)s`, but it can be customized to prepend with date and time, organize into subdirectories, etc.

+ `alembic.timezone`: An optional timezone name (e.g., UTC) that will be applied to the timestamp which renders inside the migration file's comments as well as within the filename.

+ `alembic_slug_length`: The max number of characters to include in the slug, which defaults to 40.

+ `alembic.sqlalchemy.url`: A URL to connect to the DB via SQLAlchemy. Note that this config value is used only if the `env.py` file calls upon them (which is the default).

    If the SQLAlchemy URL should come from some other place (e.g., environment variable, etc.), you are encouraged to alter `env.py` to use whatever method is appropriate to acquire the DB URL. In particular, `config.get_main_option("sqlalchemy.url")` and `engine_from_config(prefix="sqlalchemy.")` should be changed in `run_migrations_offline()` and `run_migrations_online()` respectively.

| NOTE: |
| :---- |
| For starting up with just a single DB and the generic configuration, you just need to update `alembic.sqlalchemy.url` key. |

#### Using `pyproject.toml` for configuration

To start with a `pyproject.toml` configuration you just need to do:

```bash
alembic init --template pyproject alembic
```

This will include certain configuration in your `pyproject.toml`, while other parts (such as `sqlalchemy.url`) will still be placed in your `alembic.ini`.

| NOTE: |
| :---- |
| If you modify `env.py` to obtain the DB connectivity details from other place (e.g., environment variable, `.env` file, etc.), then you can omit `alembic.ini` altogether.<br>As that is the desired end-goal for mid-sized/big projects, using `pyproject` approach is recommended. |

```bashblock
$ uv run alembic init --template pyproject alembic
  Creating directory /home/.../009_sqlalchemy_alembic_hello/009_sqlalchemy_alembic_hello/alembic ...  done
  Creating directory /home/.../009_sqlalchemy_alembic_hello/009_sqlalchemy_alembic_hello/alembic/versions ...  done
  Generating /home/.../009_sqlalchemy_alembic_hello/009_sqlalchemy_alembic_hello/alembic/env.py ...  done
  Generating /home/.../009_sqlalchemy_alembic_hello/009_sqlalchemy_alembic_hello/alembic.ini ...  done
  Generating /home/.../009_sqlalchemy_alembic_hello/009_sqlalchemy_alembic_hello/alembic/script.py.mako ...  done
  Appending to existing /home/.../009_sqlalchemy_alembic_hello/009_sqlalchemy_alembic_hello/pyproject.toml ...  done
  Generating /home/.../009_sqlalchemy_alembic_hello/009_sqlalchemy_alembic_hello/alembic/README ...  done
  Please edit configuration settings in /home/.../009_sqlalchemy_alembic_hello//009_sqlalchemy_alembic_hello/pyproject.toml and configuration/connection/logging settings in
  /home/.../009_sqlalchemy_alembic_hello/009_sqlalchemy_alembic_hello/alembic.ini before proceeding.
```

That will add the following keys to your `pyproject.toml`:

```toml
[tool.alembic]

script_location = "%(here)s/alembic"

prepend_sys_path = [
    "."
]
```

And your `alembic.ini` will get simplified:

```ini
# A generic, single database configuration.

[alembic]

# database URL.  This is consumed by the user-maintained env.py script only.
# other means of configuring database URLs may be customized within the env.py
# file.
sqlalchemy.url = driver://user:pass@localhost/dbname


# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

### Creating a migration script

With the environment in place, you can create a new revision using the following command:

```bash
$ uv run alembic revision -m "create user_account table"
  Generating /home/.../009_sqlalchemy_alembic_hello/alembic/versions/8b471e5e82ba_create_user_account_table.py ...  done
```

That will create a new file in the `versions/` directory with the following contents:

```python
"""create user_account table

Revision ID: 8b471e5e82ba
Revises:
Create Date: 2026-04-07 08:46:31.652919

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b471e5e82ba'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
```

The file contains some header information, and a couple of empty `upgrade()` and `downgrade()` functions.

Your job is to populate `upgrade()` and `downgrade()` functions that will apply a set of changes to the DB.

The `down_revision` variable is how Alembic knows the correct order in which to apply migrations. As this is our first revision, it is initially set to `None` (i.e., Alembic will read these files and compose a list based on the `down_revision` IDs).

The following code illustrates a potential implementation for the `upgrade()` and `downgrade()` functions:

```python
def upgrade():
    op.create_table(
        "user_account",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(30), nullable=False),
        sa.Column("description", sa.String)
    )

def downgrade():
    op.drop_table("user_account")
```

Both `create_table()` and `drop_table()` are Alembic directives. Alembic provides all the basic DB migration operations via these directives, which are designed to be as simple and minimalistic as possible.

An overview of all Alembic directives can be found in [Operation Reference](https://alembic.sqlalchemy.org/en/latest/ops.html#ops) section of Alembic's docs (e.g., `alter_column()`, `add_column()`)

Note that nothing prevents you from modifying the migrations file to adapt it to your coding style:

```python
"""create user_account table.

Revision ID: 8b471e5e82ba
Revises:
Create Date: 2026-04-07 08:46:31.652919

"""

from collections.abc import Sequence

from sqlalchemy import Column, Integer, String

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8b471e5e82ba"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "user_account",
        Column("id", Integer, primary_key=True),
        Column("name", String(30), nullable=False, unique=True),
        Column("fullname", String(120), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user_account")
```

### Running your first migration

The `alembic upgrade` command will run upgrade operations, proceeding from the current database revision (in this example `None`, as the DB will be totally clean and unversioned).


You can specify the revision (e.g., `uv run alembic upgrade 8b471e5e82ba`) but you will typically refer to the *most recent* upgrade by using the `head` alias (`uv run alembic upgrade head`).

Note that at this point, your `alembic.ini` should've been updated. For the purpose of the example, we will assume you're using a SQLite DB backed by a file named `app.db`.

```ini
[alembic]

# database URL.  This is consumed by the user-maintained env.py script only.
# other means of configuring database URLs may be customized within the env.py
# file.
sqlalchemy.url = sqlite+pysqlite:///app.db
```

With that change in place, you can proceed to upgrade your DB:

```bash
$ uv run alembic upgrade head
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 8b471e5e82ba, create user_account table.
```

Behind the scenes, Alembic checks if the DB has a table called `alembic_version`, and if not, Alembic creates it.

Then, it look in this table for the current version, if any, and then calculates the path from this version to the requested one (in this case, the most recent one). It then invokes `upgrade()` as you implemented.

### Running your second migration

Let's now add an additional column to the `user_account` table to keep track of when the record was created:

```bash
$ uv run alembic revision -m "add created_at col in user_account table"
  Generating /home/.../009_sqlalchemy_alembic_hello/alembic/versions/965aa2324ea1_add_created_at_col_in_user_account_table.py ...  done
```

This will create another revision that we can implement like:

```python
"""add created_at col in user_account table.

Revision ID: 965aa2324ea1
Revises: 8b471e5e82ba
Create Date: 2026-04-07 09:16:53.131319

"""

from collections.abc import Sequence

from sqlalchemy import Column, DateTime

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "965aa2324ea1"
down_revision: str | Sequence[str] | None = "8b471e5e82ba"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "user_account",
        Column("created_at", DateTime(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user_account", "created_at")
```

And you can upgrade your DB running again:

```bash
$ uv run alembic upgrade head
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 8b471e5e82ba -> 965aa2324ea1, add created_at col in user_account table.
```

### Partial revision identifiers

It is possible to use a partial revision number to refer to a particular revision:

```bash
# to run 8b471e5e82ba
$ uv run alembic upgrade 8b4
```

Alembic will complain if there are more than one versions that start with the prefix you provided.

### Relative migration identifiers

Relative upgrades/downgrades are also supported

```bash
# move two versions from the current
$ uv run alembic upgrade +2

# downgrade to the version previous from the current
$ uv run alembic downgrade -1

# upgrade two version from the given one
$ uv run alembic upgrade 8b4+2
```

### Getting information

You can use `alembic current` to get information about the current revision:

```python
# succinct output
$ uv run alembic current
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
965aa2324ea1 (head)

# verbose
$ uv run alembic current --verbose
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
Current revision(s) for sqlite+pysqlite:///app.db:
Rev: 965aa2324ea1 (head)
Parent: 8b471e5e82ba
Path: /home/.../009_sqlalchemy_alembic_hello/alembic/versions/965aa2324ea1_add_created_at_col_in_user_account_table.py

    add created_at col in user_account table.

    Revision ID: 965aa2324ea1
    Revises: 8b471e5e82ba
    Create Date: 2026-04-07 09:16:53.131319

```

You can review the migration history using `alembic history` which also accepts the `--verbose` option:

```python
# succinct
$ uv run alembic history
8b471e5e82ba -> 965aa2324ea1 (head), add created_at col in user_account table.
<base> -> 8b471e5e82ba, create user_account table.

# verbose
$ uv run alembic history --verbose
Rev: 965aa2324ea1 (head)
Parent: 8b471e5e82ba
Path: /home/.../009_sqlalchemy_alembic_hello/alembic/versions/965aa2324ea1_add_created_at_col_in_user_account_table.py

    add created_at col in user_account table.

    Revision ID: 965aa2324ea1
    Revises: 8b471e5e82ba
    Create Date: 2026-04-07 09:16:53.131319

Rev: 8b471e5e82ba
Parent: <base>
Path: /home/.../009_sqlalchemy_alembic_hello/alembic/versions/8b471e5e82ba_create_user_account_table.py

    create user_account table.

    Revision ID: 8b471e5e82ba
    Revises:
    Create Date: 2026-04-07 08:46:31.652919
```

The `history` command also allows you view history ranges:

```bash
# using explicit (partial) rev numbers
$ uv run alembic history -r 8b47:965a
8b471e5e82ba -> 965aa2324ea1 (head), add created_at col in user_account table.
<base> -> 8b471e5e82ba, create user_account table.

# using relative ranges
$ uv run alembic history -r-1:current
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
8b471e5e82ba -> 965aa2324ea1 (head), add created_at col in user_account table.
<base> -> 8b471e5e82ba, create user_account table.

$ uv run alembic history -r current:head
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
8b471e5e82ba -> 965aa2324ea1 (head), add created_at col in user_account table.
```

### Downgrading

The command `alembic downgrade` can be used to bring back the DB to any desired state:

```bash
$ uv run alembic downgrade 8b47
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade 965aa2324ea1 -> 8b471e5e82ba, add created_at col in user_account table.
```

### Auto generating migrations

While the previous approach illustrates the way in which you can create your migrations manually, the vast majority of Alembic environments rely on the autogenerate feature.

When using this feature, Alembic can view the status of the database (as identified in your `sqlalchemy.url`) compare against the table metadata as defined in your application, and generate the migrations based on a comparison.

This is achieved using the `--autogenerate` option in the `alembic revision` command (which creates the migration scripts).

In our application, we have a declarative base directly declared in `main.py`. We will need to update our `alembic/env.py` so that it gets access to that metadata object that contains the desired target state of the DB.

For your convenience, `alembic/env.py` includes a section with the following:

```python
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None
```

In our case, we will need to do:

```python
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from main import Base

target_metadata = Base.metadata
```

| NOTE: |
| :---- |
| In a real project, you will use something like `from myapp.mydel import Base`. |

With that, you'll be prepared to run an autogenerated migration:

| NOTE: |
| :---- |
| The DB must be up-to-date (in head) before running the command or you'll get a ERROR [alembic.util.messaging] Target database is not up to date.
  FAILED: Target database is not up to date.. |

```python
$ uv run alembic revision --autogenerate -m "Bring DB schema up-to-date with app"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.schemas
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.tables
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.types
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.constraints
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.defaults
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.comments
INFO  [alembic.autogenerate.compare.tables] Detected added table 'address'
INFO  [alembic.autogenerate.compare.tables] Detected removed column 'user_account.created_at'
  Generating /home/.../009_sqla
  lchemy_alembic_hello/alembic/versions/7c9419189b78_bring_db_schema_up_to_date_with_app.py ...  done
```

We can then review the contents of the newly generated migration script, to check it's done a pretty decent job:

```python
"""Bring DB schema up-to-date with app

Revision ID: 7c9419189b78
Revises: 965aa2324ea1
Create Date: 2026-04-07 10:16:49.220049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c9419189b78'
down_revision: Union[str, Sequence[str], None] = '965aa2324ea1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email_address', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('user_account', 'created_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_account', sa.Column('created_at', sa.DATETIME(), nullable=True))
    op.drop_table('address')
    # ### end Alembic commands ###
```

At that point, you can adjust whatever it's necessary. For example, it hasn't noticed that we created a unique index on `user_account.name`.

#### What does `--autogenerate` detect and what does not detect?

Autogeneration is meant to be a helper, rather than a helper tool.

According to Alembic's docs, **it is always necessary** to manually **review and correct** the candidate migration that autogenerate produces.

You should be aware of what autogenerate will detect, what can optionally detect, and what cannot detect:

Autogenerate will detect:
+ Table additions, removals.
+ Column additions, removals.
+ Change of nullable status on columns.
+ Basic changes in indexes and explicitly named unique constraints.
+ Basic changes in foreign key constraints.

Autogenerate can optionally detect:
+ Change on column types (which will happen by default).
+ Change of server default, which will happen if you set the `EnvironmentContext.configure.compare_server_default` parameter to `True` or to a custom callable function (see the documentation for details).

Autogenerate will not detect:
+ Changes of table name. These will come out as an add/drop of two different tables and should be hand-edited into a name change as needed.

+ Changes of column names. Similarly to table name changes, these are detected as column add/drop pair.

+ Anonymously named constraints.In order to prevent these caveat, make sure to give your constraints a name (e.g., `UniqueConstraint("col1", "col2", name="my_unique_index")`).

    For example, you should have declared the uniqueness of the `name` column as:

    ```python
    user_account = Table("user_account", meta,
                  Column("id", Integer, primary_key=True),
                  Column("name", String(50)),
                  UniqueConstraint("name", name="uq_user_account_name")
              )
    ```

+ Special SQLAlchemy types such as `Enum` when generated on a backend that doesn't support ENUM directly.

+ Some free-standing constraint additions and removals (including PRIMARY KEY, EXCLUDE, CHECK), although there's work in progress to support this.

+ Sequence additions, removals. There's work in progress to support this.

Note also that there are certain 3rd party libraries that can be used to support additional things such as:

+ `alembic-utils`: Library to add autogenerate support for Postgres functions, views, triggers...
+ `alembic-postgresql-enum`: Library that adds autogenerate support for creation, alteration, and deletion of `Enum`s in Postgres.

Finally see the following sections to control what to be autogenerated:
+ [Controlling what to be autogenerated](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#controlling-what-to-be-autogenerated)

+ [Omitting schema names from the autogenerate process](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#omitting-schema-names-from-the-autogenerate-process)

+ [Omitting table names from the autogenerate process](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#omitting-table-names-from-the-autogenerate-process)

+ ...

#### Applying post processing and python code formatters to generated revisions

The scripts generated by the `alembic revision` command, can be optionally piped through a series of post-production functions which may analyze or rewrite Python source code generated by Alembic.

This is intended to allow you to apply formatting and linting rules to the files.

The template samples for `alembic.ini` and `pyproject.toml` include commented-out configuration illustrating how to configure code-formatting tools to run against the newly generate file path.

Note also, that you can always do that manually, as you are ultimately responsible for reviewing and adapting those migration scripts.

You can find examples in the [docs](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#omitting-table-names-from-the-autogenerate-process).

### Running checks before the upgrade operation

Alembic provides the `alembic check` command, which will run through the same process as `alembic revision --autogenerate`, but will not generate any new files. Instead, it will return an error code and a message if it detects that a new revision will be required to bring the DB in sync with your app, or a success code if your app is in sync with your DB:

```bash
# app not in sync with your DB
$ uv run alembic check
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
ERROR [alembic.util.messaging] Target database is not up to date.
  FAILED: Target database is not up to date.

# app in sync with your DB
$ uv run alembic check
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.schemas
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.tables
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.types
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.constraints
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.defaults
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.comments
No new upgrade operations detected.
```

### The "offline mode"

A major capability of Alembic is to generate migrations as SQL scripts, instead of running them against the DB.

This is needed in large organization scenarios where migrations scripts should be handed off to DBAs for their review and execution, as access to DDL might be restricted.

You can do so with the `--sql` option:

```
$ uv run alembic upgrade head --sql
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Generating static SQL
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

INFO  [alembic.runtime.migration] Running upgrade  -> 8b471e5e82ba, create user_account table.
-- Running upgrade  -> 8b471e5e82ba

CREATE TABLE user_account (
    id INTEGER NOT NULL,
    name VARCHAR(30) NOT NULL,
    fullname VARCHAR(120) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (name)
);

INSERT INTO alembic_version (version_num) VALUES ('8b471e5e82ba') RETURNING version_num;

INFO  [alembic.runtime.migration] Running upgrade 8b471e5e82ba -> 965aa2324ea1, add created_at col in user_account table.
-- Running upgrade 8b471e5e82ba -> 965aa2324ea1

ALTER TABLE user_account ADD COLUMN created_at DATETIME;

UPDATE alembic_version SET version_num='965aa2324ea1' WHERE alembic_version.version_num = '8b471e5e82ba';

INFO  [alembic.runtime.migration] Running upgrade 965aa2324ea1 -> 7c9419189b78, Bring DB schema up-to-date with app
-- Running upgrade 965aa2324ea1 -> 7c9419189b78

CREATE TABLE address (
    id INTEGER NOT NULL,
    email_address VARCHAR(50) NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES user_account (id)
);

ALTER TABLE user_account DROP COLUMN created_at;

UPDATE alembic_version SET version_num='7c9419189b78' WHERE alembic_version.version_num = '965aa2324ea1';
```

You can use `alembic upgrade 965aa2324ea1 --sql > migration.sql` to get the DDL written to `migration.sql` file.

### Data migration considerations

Alembic migrations are designed for schema migrations. The nature of data migrations are inherently different, and it's not advisable in the general case to write data migrations that integrate with Alembic's schema versioning model.

In particular, downgrades will be difficult to address since they might require deletion of data, which may not even be possible to detect.

There are however, three basic techniques that might come in handy.

#### Small data

Small data migrations are easy to perform, especially in cases where you need initial data added to a new table.

These are typically handled using `Operations.bulk_insert()`:

```python
op.bulk_insert(
    user_table,
    [
        {"id": 1, "name": "spongebob", "fullname": "Spongebob Squarepants"},
        {"id": 2, "name": "patrick", "fullname": "Patrick Star"},
        {"id": 3, "name": "sandy", "fullname": "Sandy Cheeks"},
    ],
)
```

See [Bulk Insert](https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.bulk_insert) for additional details.

#### Separate migration script

One possibility is a completely separate script aside of alembic migrations.

In those case, the complete migration process will be as follows:

1. Run the initial alembic migrations (new columns, etc.).
1. Run the separate data migration script.
1. Run the final alembic migrations (database constraints, delete columns, etc.).

#### Online migration

The app maintains a version of schema with both versions. Writes are performed on both places, while the background script move all the remaining data across.

This technique is very challenging and time demanding, since it requires custom app logic to handle intermediate states.