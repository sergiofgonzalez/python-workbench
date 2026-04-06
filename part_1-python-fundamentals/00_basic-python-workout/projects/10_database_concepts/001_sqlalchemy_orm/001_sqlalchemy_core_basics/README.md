# 001: Hello, SQLAlchemy Core basics
> Illustrates the basics of SQLAlchemy Core: Connections, issuing statements, committing, transactions

## Project description

This lab illustrates the basics of SQLALchemy Core module:
+ Creating the engine
+ Getting a connection
+ Using *commit as you go* and *begin once* approaches for committing
+ Issuing basic SQL statements
+ Using parameters in your queries

### A simple walkthrough of SQLAlchemy core basics

#### Instantiating the SQLAlchemy `Engine`

The `Engine` is a global object whose purpose is to enable you to interact with a particular DB server.

Create an engine to connect to SQLite using its in-memory only model. In the connection string, specify that you want to use the modern `pysqlite` interface. Also, configure SQLAlchemy to output the SQL statements it issues.


#### Obtaining a `Connection` and issuing a simple query with `execute()`

The `Connection` object is obtained from the engine and supports the resource manager protocol.

Create a connection object to the database and run the query:

```SQL
SELECT "hello world"
```

#### Issuing your first `INSERT` statement and committing your changes as you go

By default, when using a connection with the resource manager protocol, the transaction will be rolled back so no changes will be persisted.

Create your first transaction consisting of:
1. Creating a table `some_table` with columns x and y both integers.
1. Issue an insert statement with values x=1, y=1
1. Issue an insert statement with values x=2, y=4 and x=3, y=9 in the same statement.
1. Commit your changes

#### Using the *begin once* technique

Insert in `some_table` the value x=4, y=16 and x=5, y=25 using the *begin once* technique.

#### Fetching the results using for ... in

Retrieve all the rows from `some_table` using the `Result` as an Iterable object of result rows. For reading the results, use the attribute names (as if they were attributes of a class).

Repeat the exercise retrieving the results from each `Row` using:
+ tuple access (using unpacking with the `Row` object)
+ their integer index
+ their mappings (as if they were dicts)


What's the difference between issuing the statement and iterating through the results and using `Result.all()`?

SOLUTION:

When invoking `Result.all()` the engine materializes all the results as tuples

#### Sending (bound) parameters

Familiarize yourself with how parameters are sent to SQLAlchemy queries using the following queries:

```sql
SELECT x, y FROM some_table
 WHERE y > :y
```

where `:y` should be greater than 2.

```sql
INSERT INTO some_table (x, y)
VALUES (:x, :y)
```

to insert the values x=6, y=36, and x=7, y=49.


## Running the program

You can run the application with:

```bash
uv run main.py
```

## Project management

This project is managed using `uv`.

FastAPI dependency was added using:

```bash
$ uv add SQLAlchemy
```

as I don't intend to use FastAPI cloud at the moment.

The only other dependency was ruff:

```bash
$ uv add ruff --dev
```
