# 005: Hello, SQLAlchemy UPDATE/DELETE statements
> Illustrates the basics of UPDATE and DELETE statements with SQLAlchemy

## Project description

This lab illustrates the basics of UPDATE/DELETE statements when using SQLAlchemy Core module.



### Setting up shop

1. Create an engine to connect to SQLite using a file called `app.db`.

1. Create the `MetaData` object, and the necessary programmatic code to create a `user_account` table with the following details:
    + id: int, primary key of the table
    + name: str, 30 chars long
    + fullname: str, no max length

1. Create an `address` table with fields:
    + id: int, primary key.
    + email_address: str, not null
    + user_id: foreign key to user_account's id field, not null


1. Populate the `user_account` table with the following data:
  + 1,spongebob,"Spongebob Squarepants"
  + 2,patrick,"Patrick Star"
  + 3,sandy,"Sandy Cheeks"
  + 4,squidward,"Squidward Tentacles"
  + 5,gary,"Gary the Snail"
  + 6,mrkrabs,"Eugene Krabs"
  + 7,pearl,"Pearl Krabs"

1. Populate the `address` table with the following data:
  + 1,spongebob@example.com,1
  + 2,squidward@example.com,4
  + 3,pearl@example.com,7
  + 4,sandy@example.com,3
  + 5,pearl@foo.com,7
  + 6,sandy@bar.com,3

### UPDATE basics

1. Write and execute the code that updates the fullname value of the `user_account` table to "Patrick the Star" for the name "patrick".
1. Write and execute the code that updates the fullname to a column expression "Username:" + name for the user whose name is "patrick".
1. Write and execute the query that performs the following updates in a single shot using the "executemany" technique:

    + oldname: "sandy" -> newname: "sandee"
    + oldname: "patrick" -> newname: "pat"
    + oldname: "squidward" -> newname: "squid-edward"

    Note that you will need to use `bindparam()` to support this technique.

### Correlated updates

A correlated update is an update that uses rows from another table. This requires the use of a subquery.

Write the query that updates the `user_account` table by setting the fullname to the result of getting the first email_address from the `address` table whose address.user_id == user_account.id.

### DELETE basics

1. Write the query that deletes from the user_account the row whose name is "patrick". How does that leave the address_table?

SOLUTION:
Address table is left with an orphan row that is pointing to a user_id that no longer exists.

1. Write the query that deletes from the user_account the row whose name is "ed". What error do you get?

SOLUTION:
No error. A DELETE statement does not fail when the row doesn't exist.

### Correlated deletes

Write the correlated query that deletes from the `user_account` table the user whose id matches the user_id from the `address_table` and whose address is "patrick@example.com".

### Getting the affected rows from UPDATE, DELETE. Using RETURNING.

1. Write the query that updates in the `address` table the user whose name is "pearl" and print the number of affected rows.
1. Write the query that updates in the `user_account` table the user whose name is "mrkrabs" and returns the fullname and the id.
1. Write the query that deletes from the `user_account` table the user whose name is "spongebob" returning the id, and fullname of the record deleted.

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
