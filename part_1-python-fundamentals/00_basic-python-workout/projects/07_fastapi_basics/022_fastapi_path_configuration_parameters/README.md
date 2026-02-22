# 022: Hello, FastAPI path configuration parameters
> Illustrates the basics of path configuration

## Project description

This project illustrates how to configure path parameters through the path operation decorator parameters.

### Configuring the response status code

Create a path operation `POST /items/` for the creation of an item that returns a 201 Created, instead of 200 OK.

### Tags

Create path operations for:
+ creation of an item, tags should be "items"
+ retrieval of all the items, tags should "items"
+ retrieval of users, tags should be "users"

Check the /docs to see how the operations are classified in the docs.

Repeat the exercise using enums instead of plain strings.

### Summary and description

Create a path operation for the creation of an item and include both a summary and description using parameters.

Repeat the exercise using the function docstrings.

Check in both cases how the information shows up in /docs.

Finally, use `response_description` to document the response and check how it shows up in the docs.

### Deprecating a path operation

Create a path operation that is mark as deprecated. Check that it can still be used.

Check how this shows up in the docs.

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
