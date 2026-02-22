# 026: Hello, FastAPI dependencies as classes
> Illustrates the basics of implementing dependencies with classes

## Project description

FastAPI's Dependency Injection system works with any type of callable (including classes). This project illustrates how to work with classes.

### Implementing dependencies as classes

Create a FastAPI app in which you define a class `CommonQueryParams` that you intend to use as a dependency to manage pagination.

It should include:
+ q: optional str, representing how to filter the data
+ skip: optional int, default value 0, where the results should start.
+ limit: optional int, default value 100, the number of results

Then create a `GET /items/` path operation that:
+ if q is given, it's included in the response
+ then returns the items from a fake_items_db object that contains a bunch of items using the values from the `CommonQueryParams`.

SOLUTION:

You can test this with:

```bash
# Remember, q, skip, limit are query parameters
$ http get :5000/items/ q=="query" skip==1 limit==3
```

## Running the program

You can run the application with:

```bash
uv run fastapi dev main.py --port {port}
```

## Project management

This project is managed using `uv`.

FastAPI dependency was added using:

```bash
$ uv add fastapi[standard-no-fastapi-cloud-cli]
```

as I don't intend to use FastAPI cloud at the moment.

The only other dependency was ruff:

```bash
$ uv add ruff --dev
```
