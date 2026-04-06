# 004: SQLALchemy: SELECT statements
> Basics of SELECT statement in SQLALchemy

## Project description

The `select()` function is used to run SELECT queries. When you invoke that function, a `Select` object will be instantiated which you will be able to pass to `execute()` to get a `Result` object, which will ultimately give you access to the `Row` objects.

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


### Simple SELECT / SELECT ... FROM ... WHERE ...

1. Execute the SELECT statement that retrieves all the records from the `user_account`.

1. Execute the SELECT statement that retrieves the record from `user_account` where name = "spongebob".

1. Execute the SELECT that retrieves the `name` and `fullname` columns from the `user_account` table using both the syntax that lets you pass the columns individually, and the `[]` syntax.

1. Use the `[]` syntax to allow the user to choose the columns to show from the `address` table.

### Getting the results of a SELECT query: `first()`, `all()`.

1. Write the code that retrieves the first result of a SELECT query over all the records of the `user_account` table, and check the type of the result.

1. Write a query that materializes the first row resulting from querying the `user_account` table with a SELECT statement.


### Ordering results with `order_by()`

1. Write the code that selects the `name` from `user_account` and all the fields from `address` where the `id` from `user_account` matches the `user_id` on the `address` table. Make sure you think about what should be the result of the join before executing.

1. Update the query to order the result by `id` of the address.


### Using `label()`

1. Write the code that retrieves the value `"Username: {name}"` where `name` is the column from the `user_account` table, ordered by `name`.

1. Update the query so that the value is labeled as `username` and iterate over the results using the attribute syntax.

### Using `text()`

Write a query that retrieves the text "some phrase" and the `name` column from the `user_account` table, ordered by the name.

Print the results.

### Using `literal_column()`

Write a query that retrieves the text "some phrase" and the `name` column from the `user_account` table, ordered by the name using `literal_column()`.

Label the column with the text as `"p"` and use it when printing the results.

Print the results.

### Using `where()`, `and_()` and `or_()`

1. Write the query that reads all records from `user_account` whose `name` is "squidward".

1. Write the query that reads all records from `user_account` whose `id` is >= 5.

1. Write the query that reads the `email_address` field from `address` table where `name` is "squidward" and the `user_id` is equal to the `id` in the `user_account` table, using multiple `where()` invocations.

1. Repeat the exercise using a single `where()` with two arguments.

1. Write the query that reads the `email_address` where the name of the user is "squidward" or "sandy" and the user_id = id (the right hand side is the id of the `user_account` table).

### Using filter_by()

Use `filter_by` to query the records from the `user_account` table where name is "spongebob" and fullname is "Spongebob Squarepants".

### JOINs and explicit FROM clauses: `join_from()`, `join()`, `select_from()`

1. Write the code to perform a JOIN from `user_account` and `address` showing all the columns. This will return the cartesian product of both tables (no WHERE or JOIN ON specified).

1. Repeat the exercise, showing only the `name` (`user_account`) and `email_address` (`address`). This will return the cartesian product of both tables (no WHERE or JOIN ON specified).

1. Rewrite the query using `join_from()` and confirm you that the JOIN ... ON is added.

1. Rewrite the query using `join()` and confirm you get the same results.

1. Write the query that counts how many records are available in the `user_account` table (HINT: use `select_from()`).

1. Write a query that retrieves the `email_address` column where you join `user_account` and `address` where the join is done on `id = user_id` (left-hand is the `id` from `user_table`). (HINT: pass a second argument to `join_from()`)

### Types of JOINs

1. Prepare a couple of tables with the following details:
  + num_esp
    + `id`, int, primary key
    + `desc`, str
  + num_eng
    + `id`, int, primary key
    + `desc`, str

1. Populate with the following data:

    ```
    (1, "uno")     (1, "one")
    (2, "dos")     (2, "two")
    (3, "tres")    (4, "four")
    ```

1. Using SQL (e.g., from DBveaver) get the results of:

    1. SELECT * FROM num_esp, num_eng (no WHERE to see the cartesian product)

        ```
        1,uno,1,one
        1,uno,2,two
        2,dos,1,one
        2,dos,2,two
        3,tres,3,two
        ```


    1. Implicit JOIN: This form is discouraged, explicit JOIN should be used instead.

        ```sql
        SELECT * FROM num_esp left, num_eng right
         WHERE left.id = right.id
        ```

        Results:
        ```
        1,uno,1,one
        2,dos,2,two
        ```

    1. Explicit INNER JOIN: The matching results need to be in both tables. It's the same as JOIN

        ```sql
        /* INNER JOIN */
        SELECT * FROM num_esp a
        INNER JOIN num_eng b
        WHERE a.id = b.id

        /* (explicit) JOIN */
        SELECT * FROM num_esp a
        INNER JOIN num_eng b
        WHERE a.id = b.id
        ```

        ```
        1,uno,1,one
        2,dos,2,two
        ```

    1. LEFT OUTER JOIN: The left table will drive the result set, in the sense that if a record from the left table does not have a counterpart on the right table, a null will be returned:

        ```sql
        /* LEFT JOIN is the same as LEFT OUTER JOIN */
        SELECT *
        FROM num_esp a
        LEFT JOIN num_eng b
        ON a.id = b.id

        /* LEFT JOIN is the same as LEFT OUTER JOIN */
        SELECT *
        FROM num_esp a
        LEFT OUTER JOIN num_eng b
        ON a.id = b.id
        ```


        ```
        1,uno,1,one
        2,dos,2,two
        3,tres,[null],[null]
        ```


    1. RIGHT OUTER JOIN: The right table will drive the result set, in the sense that if a record from the right table does not have a counterpart on the left table, a null will be returned:

        ```sql
        /* RIGHT JOIN is the same as RIGHT OUTER JOIN */
        SELECT *
        FROM num_esp a
        RIGHT JOIN num_eng b
        ON a.id = b.id

        /* RIGHT JOIN is the same as RIGHT OUTER JOIN */
        SELECT *
        FROM num_esp a
        RIGHT OUTER JOIN num_eng b
        ON a.id = b.id
        ```


        ```
        1,uno,1,one
        2,dos,2,two
        [null],[null],4,four
        ```

        Note that a RIGHT OUTER JOIN is a LEFT OUTER JOIN where the left and right tables have been swapped:

        ```sql
        SELECT *
        FROM num_eng a
        RIGHT OUTER JOIN num_esp b
        ON a.id = b.id
        ```


        ```
        1,one,1,uno
        2,two,2,two
        [null],[null],3,tres
        ```


    1. FULL OUTER JOIN: In a full outer join, unmatched values from both left and right tables will be included in the result set.

        ```sql
        SELECT *
        FROM num_eng a
        FULL OUTER JOIN num_esp b
        ON a.id = b.id
        ```

        ```
        1,one,1,uno
        2,two,2,two
        3,tres,[null],[null]
        [null],[null],4,four
        ```

    Try to predict the results of the queries before running them.

1. Rewrite the SQL queries using SQLAlchemy

1. Write an INNER JOIN on `user_account` and `address`.
1. Write a LEFT OUTER JOIN on `user_account` and `address`.
1. Write a FULL OUTER JOIN on `user_account` and `address`.
1. Write a FULL OUTER JOIN on `user_account` and `address` using the `.outerjoin()` method.

### ORDER BY

Practice the `order_by()` method by

1. Order the results from `user_account` ordering by `name`.
1. Order the results from `user_account` ordering by `name`, in descending order.
1. Order the results from `user_account` ordering by `name`, in ascending order.

### GROUP BY / HAVING

Familiarize yourself with how GROUP BY / HAVING works with SQLAlchemy core by:


1. Create a function to count id's in user table.
1. Execute the query that selects the count function.
1. Write the code that selects user name fields and their corresponding count of addresses using group by.
1. Write the code that selects user name fields and their corresponding count of addresses using group by, for users having more than one email.
1. Write the code that selects user name fields and their corresponding count of addresses using group by, for users having zero addresses.
1. Write the code that selects user name fields and their corresponding count of addresses using group by, ordered by `user_id` and then by number of addresses in descending order.

### Using aliases

Familiarize yourself with aliases by writing the code that that returns all unique pairs or user names when you join `user_account` with itself.

### Using non-scalar subqueries

Familiarize yourself with non-scalar subqueries. These are most commonly used in the FROM clause of an enclosing SELECT statements.

1. Create the subquery that returns the count of addresses for each user_id, grouped by user_id.
1. Print the subquery
1. Use it in an enclosing SELECT in which you get the name, fullname, count column from the subquery, (HINT: you'll need to join the subquery).

### Using CTEs

Common Table Expressions (CTEs) in SQLAlchemy can be used as a FROM element in an enclosing select, but using a different underlying syntax.

1. Create a CTE that returns the count of addresses for each user_id, grouped by user_id.
1. Print the subquery
1. Use it in an enclosing SELECT in which you get the name, fullname, count column from the subquery (HINT: you'll need to join both tables).

### Scalar queries

A scalar query is a subquery that returns exactly zero or one row. Those are typically used in the cloumns or WHERE clause of an enclosing SELECT statement.

They're commonly found when you use aggregate functions such as count, average, min, max, etc.

1. Write the scalar subquery that returns the number of `id`'s in the `address_table` for which the `id` matches the `id` in the `user_account` table.
1. Print the resulting scalar subquery.
1. Write the (correlated) scalar subquery returns the number of `id`'s in the `address_table` for which the `id` matches the `id` in the `user_account` table. HINT: you may need to use `correlate()`.
1. Write and execute the query that selects `name`, `email_address`, and `address_count` (from the subquery), by joining `user_account` and `address_table` and order the results by `user_account` `id` and `address_table` id.

### UNION and UNION ALL

Familiarize yourself with UNION in SQLAlchemy by
1. Create a query that returns the union of the query that selects all the data from `user_account` for the names that begin with "s" and "p"
1. Use the previous query as a subquery (HINT: use `.subquery()`)
1. Write the query that retrieves `name`, `email_address` from `address_table`


### EXISTS subqueries

Familiarize yourself with scalar subqueries (the ones that return a boolean true or false) by:
1. Writing the query that returns the users with no email.
1. Writing the query that returns the users with more than one email
1. Use it to create a report by using that query as a subquery.


### SQL functions

Familiarize yourself with functions in SQLAlchemy by:

1. Run the query that counts all the users whose name begin with "p"
1. Run the query that transforms the string "Hello to Jason Isaacs!" to lowercase.
1. Run the query that transforms all names to uppercase
1. Run the query that returns the current date and time
1. Inspect the return type of `func.concat()` and `func.now()`.

### Window functions

Familiarize yourself with the use of window functions by:
1. Running the code that uses `func.row_number()` and `over(partition_by=...)` to count each of the emails associated to each user. That is, you should select row number, name, and address and make row_number change in every window delimited by the change of user email.
1. Running the code that uses `func.count()` and `over(order_by=...)` to count the rows by name. That is, That is, you should select count, name, and address and make count change with every window delimited by the change of user email.

### Data casts and type_coerce()

1. Write a query that returns all the id's from the user_table as Strings.
1. Rewrite the query to use `type_coerce()`. Print, compare, and execute.
1. Write the cast of the object {"a": "b"} as a JSON object (HINT: you will need to import JSON from sqlalchemy). This might not work in some DB backends.
1. Write the query that returns the value associated to the key "a". This might not work in some DB backends.


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
