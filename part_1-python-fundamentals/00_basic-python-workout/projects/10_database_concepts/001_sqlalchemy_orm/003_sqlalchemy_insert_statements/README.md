# 003: SQLAlchemy: Working with data: INSERT statements
> Illustrates the basics of SQLAlchemy INSERT statements

## Project description

This lab illustrates the basics of the `insert()` function which represents a SQL INSERT statement, and ultimately is used to add new data into a table.

### Practicing SQLAlchemy `insert()`

1. Create an engine to connect to SQLite using a file called `app.db`.

1. Create the `MetaData` object, and the necessary programmatic code to create a `user_account` table with the following details:
    + id: int, primary key of the table
    + name: str, 30 chars long
    + fullname: str, no max length

1. Create an `address` table with fields:
    + id: int, primary key.
    + user_id: foreign key to user_account's id field, not null
    + email_address: str, not null

1. Emit the DDL to create all the tables and confirm that the tables have been created.

1. Insert in the `user_account` table the record using `insert(...).values()`:
    + name: spongebob
    + fullname: Spongebob Squarepants

1. Print the resulting statement

1. Get the result of invoking `compile()` on the statement.

1. Print the `params` of the compiled statement.

1. Check if the `insert()` function returns something (HINT: the `inserted_primary_key`).

1. Insert two records into `user_account` with a single statement using only an `insert()` (no `.values()` part!):
    + name: sandy, fullname: Sandy Cheeks
    + name: patrick, fullname: Patrick Star

1. Check if the `insert()` function returns something (HINT: the `inserted_primary_key_rows`).

1. Confirm that when passing multiple records to an execute-many only the first record is evaluated to build the `VALUES` part of the `INSERT` statement.

### Practicing complex INSERT statements: using scalar subqueries

In this section, you build a query to insert data into the `address` table by getting values from the `user_account` table. That is, you will:
+ insert into `address`, populating `username`, `email_address`, and `user_id`.
+ where user_id is the `id` in `user_account` where `name` is equal to the username given.

1. Build the scalar subquery that gets the `id` given the `username` from the `user_account`. You will need to rely on `bindparam()` to identify the bound parameter from the outer query that will be injected into the scalar subquery to get the result. Also, you will need to use `scalar_subquery()` so that a value (instead of a `Row`) is returned. That way, you will be able to inject it in the subsequent query.

1. Build the insert query on the `address` table. You will need to use both `value()` and a list of bound parameters. In the values, you will identify the `user_id` column and the result of the scalar subquery. In the parameters, you will use the regular data to be inserted.

### Practicing complex INSERT statements: using INSERT...RETURNING

In this section, you build an INSERT...QUERY to explicitly tell the DB server that you want the INSERT statement to return certain data generated as part of the INSERT.

Create a statement to insert into the address table using the statement from [using scalar subqueries](#practicing-complex-insert-statements-using-scalar-subqueries) that requests returning:
+ `id`
+ `email_address`

### Practicing complex INSERT statements: using INSERT...FROM SELECT

In this section, you build an INSERT...FROM SELECT to copy data from some other part of the DB directly into a new set of rows, without actually fetching and re-sending the data from the client.

Create an INSERT statement that inserts in `address` records with `user_id`, `email_address` that are being taken from the `user_account` table where the email is generated from the `name` from `user_account` concatenated with `@example.com` using `insert(...).from_select()`.

NOTE: you will get duplicated entries after the 

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
