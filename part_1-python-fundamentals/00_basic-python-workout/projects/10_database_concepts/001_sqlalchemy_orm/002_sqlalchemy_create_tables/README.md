# 002: Hello, creating tables in SQLAlchema
> Illustrates the basics of using creating tables in SQLAlchemy

## Project description

This lab illustrates how to create tables in different ways:
+ programmatically
+ declaratively
+ using reflection

Each section of the lab will use a different approach and will use a different entry point.

### Creating tables programmatically

In this example, you will create a `user_account` and `address` table programmatically. The `address` table will feature a foreign key constraint to the user_account's id field.

1. Create a `main_programmatic.py` for the lab.

1. Create an engine pointing to a SQLite, in-memory DB. Make sure to select the pysqlite interface.

1. Create the `MetaData` object globally in your main program.

1. Create a `user_account` table with the following structure.
    + id: int, primary key of the table
    + name: str, 30 chars long
    + fullname: str, no max length

1. Create an `address` table with fields:
    + id: int, primary key.
    + user_id: foreign key to user_account's id field, not null
    + email_address: str, not null

1. Emit the DDL to create all the tables and confirm that the tables have been created.

1. Emit the DDL to drop all the tables and confirm that the tables have been dropped.


Are the columns nullable or not nullable by default? How can you check that tables have been created or dropped?

SOLUTION:

Inspecting the issued DDLs:

```sql
CREATE TABLE user_account (
        id INTEGER NOT NULL,
        name VARCHAR(30),
        fullname VARCHAR,
        PRIMARY KEY (id)
)
```

we can see that `name` and `fullname` are nullable. Therefore, `nullable=True` by default, so you have to explicitly specify the columns that should be `NOT NULL` (just as in SQL).

By setting `echo=True` when creating the engine, you can see the DDLs being issued, so you can assume the tables are being created and dropped.

However, if you want to confirm it by other means, you can change the SQLite to use a file and use sqlite3 CLI or other graphical tool such as dbeaver.

You can install dbeaver in WSL using the information in https://dbeaver.io/download/

```bash
$ sudo snap install dbeaver-ce --classic
```

Then you can do:

```bash
$ dbeaver-ce
```

And configure the connection to open the file that represents the DB and you'll be able to see your `user_account` and `address` tables. After having execute the `drop_all()` the tables will be gone.


### Creating tables declaratively.

In this example, you will create a `User` and `Address` mapped classes using the declarative approach that will be used in SQLAlchemy ORM.

1. Create a `main_orm.py` for the lab.

1. Create an engine pointing to a SQLite, in-memory DB. Make sure to select the pysqlite interface.

1. Create a `Base` class representing the `MetaData` object by subclassing `DeclarativeBase`.

1. Create a `User` class with the following structure:
    + table name: user_account
    + id: int, primary key of the table
    + name: str, 30 chars long
    + fullname: str, no max length, nullable
    + addresses: list of `Address` objects (HINT: use `relationship(back_populates=...)`).

1. Create a dev-friendly representation of the fields of the object (HINT: don't include `addresses` as that's owned by another object.)

1. Create an `Address` class with the following structure
    + table name: address
    + id: int, primary key.
    + email_address: str
    + user_id: mapped column to `user_account.id` to declare it's a foreign key to that column field.

    + user: mapped to `User` (HINT: use `relationship(back_populates=...`)

1. Create a dev-friendly representation of the fields of the object (HINT: don't include `user` as that's owned by another object.)

1. Emit the DDL to create all the tables and confirm that the tables have been created.

1. Emit the DDL to drop all the tables and confirm that the tables have been dropped.


### Using reflection

In this example, you will manually create a `sample_table` and use reflection to

1. Create a `main_reflection.py` for the lab.

1. Create an engine pointing to a SQLite, in-memory DB. Make sure to select the pysqlite interface.

1. Create a `sample_table` table using `Connection.execute` with columns x and y (both ints).

1. Create the `MetaData` object programmatically.

1. Load `some_table` programmatically.

1. Emit the DDL to drop the table and confirm that the table has been dropped.

1. Emit the DDL to create the table and confirm the table has been recreated.


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
