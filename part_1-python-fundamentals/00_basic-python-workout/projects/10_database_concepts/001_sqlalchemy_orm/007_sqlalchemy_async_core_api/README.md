# 007: Hello, SQLAlchemy Async Core API
> Illustrates the basics of SQLAlchemy Async Core API

## Project description

This project illustrates the basics of SQLAlchemy's Async Core API by reimplementing some of the previous scenarios within an asyncio program.

### Creating the tables

1. Establish your asyncio program, with an `async_main()` coroutine.

1. Create a function `setup_db` that:
    1. Creates the `AsyncEngine` (scoped to the `async_main()function), pointing to a file `app.db`. Also, make sure to include the `connect` listener to change the SQLite defaults with respect to the foreign keys and WAL.
    1. Create the `MetaData` object.
    1. Declares the `user_account` table with the following details:
        + id: int, primary key of the table
        + name: str, 30 chars long, not null
        + fullname: str, no max length
    1. Declares the `address` table with the following details:
        + id: int, primary key.
        + user_id: foreign key to user_account's id field, not null
        + email_address: str, not null
    1. Emit the DDL to create all the tables and confirm that the tables have been created.

### Populating the tables

1. Populate the `user_account` table with the following data:
  + 1,spongebob,"Spongebob Squarepants"
  + 2,patrick,"Patrick Star"
  + 3,sandy,"Sandy Cheeks"
  + 4,squidward,"Squidward Tentacles"
  + 5,gary,"Gary the Snail"
  + 6,mrkrabs,"Eugene Krabs"
  + 7,pearl,"Pearl Krabs"

1. Populate the `address` table with the following data (using subqueries):
  + 1,spongebob@example.com,1
  + 2,squidward@example.com,4
  + 3,pearl@example.com,7
  + 4,sandy@example.com,3
  + 5,pearl@foo.com,7
  + 6,sandy@bar.com,3

### Selecting data from the table

1. Get all the rows from the `user_account` table using `all()`.
1. Get all the rows from the `address` table using an async iterator (Streaming API).
1. Write the query that reads `name`, `fullname`, and `email_address` and get the results using both `fetchall()` and with the streaming API.

### Update and delete statements

1. Change the user `patrick` so that the fullname becomes `Patrick the Star`.

1. Write and execute the query that performs the following updates in a single shot using the "executemany" technique:

    + oldname: "sandy" -> newname: "sandee"
    + oldname: "patrick" -> newname: "pat"
    + oldname: "squidward" -> newname: "squid-edward"

    Note that you will need to use `bindparam()` to support this technique.

1. Delete the user `pat`.

1. Delete the user whose email is `sandy@example.com` using *correlated deletes*, that is, the `where()` should include a scalar subquery that gets the user from the email.

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
