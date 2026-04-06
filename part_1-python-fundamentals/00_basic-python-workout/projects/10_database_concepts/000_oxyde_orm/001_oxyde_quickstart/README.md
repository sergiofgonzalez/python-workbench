# 001: Oxyde ORM quickstart
> simplest Oxyde ORM example illustrating how to connect and interact with the db using oxyde

## Application specs

Build a simple application using Oxyde ORM backed by SQLite illustrating how to work with oxyde.

1. Run `oxyde init` to initialize the Oxyde ORM configuration (`oxide_config.py`).

    Make sure you use relative paths when specifying the connection string for your SQLite file (e.g., sqlite://./app.db). Otherwise, Oxyde will try to write the file at the root of the file system.

1. Create an Oxyde model for a User with the following fields:
    + `id`: optional int, default should be `None`. Declare it as the PK of the corresponding table (HINT: use `db_pk=True`).
    + `name`: required str.
    + `email`: required str. It should be unique in the DB (HINT: use `db_unique=True`).
    + `age`: optional int, default should be `None`.

1. Create a `Meta` subclass within the model to declare:
    + table name, which should be `users` (HINT: use `table_name` and `is_table`).

1. Run `oxyde makemigrations` to create the migration logic.

1. Run `oxyde migrate` to apply the migrations.

1. Create `main.py` with the following logic:
    1. Connect to the db (HINT: you will need to re-specify the connection URL as you did in step 1).
    1. Create a new user by giving the name, email, and age.
    1. Print the name of the saved user and his/her `id`, which would have been populated after `create()`.
    1. Retrieve the number of users in the DB whose age is greater than 25.
    1. Update the user's age to 31.
    1. Delete the user.
    1. Close the connection to the DB.

For additional notes, please review the information in [README.md](../README.md#quick-start).


## Running the program

See [README.md](../README.md#999-TBD) for full details.

You can run the application with:

```bash
uv run main.py
```

