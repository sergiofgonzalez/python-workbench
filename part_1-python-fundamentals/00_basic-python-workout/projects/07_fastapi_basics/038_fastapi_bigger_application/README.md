# 038: Hello, FastAPI bigger application
> Illustrates how to structure a bigger FastAPI app

## Project description

This project demonstrates the recommended structure for a bigger FastAPI application with multiple files, in which path operations are separated by domains (items, users, ...) and dependencies and shared modules are hosted on their own packages.

### Creating a dummy bigger application

1. Start by manually creating the following file structure:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
|── pyproject.toml
└── README.md
```

1. Populate `app/routers/users.py` with the path operations corresponding to user management.
    1. Instantiate a plain `APIRouter()`
    1. Create dummy path operations for `GET /users/`, `GET /users/me`, `GET /users/{username}`, all tagged under the "users" group in your docs.

1. Populate your `app/dependencies.py` with:
    1. `get_token_header()`: a dependency that reads `x_token` from the headers and fails with a 400 if not present.
    1. `get_token_query()`: a dependency that reads the `token` query parameter from the request and fails with a 400 if not present.

1. Populate `app/routers/items.py` with the path operations corresponding to the item management.
    1. Instantiate an `APIRouter` but this time set the prefix, tags, dependency with the `get_token_header` and responses for 404 with the description "Not Found"
    1. In the submodule, define a fake db with a few items.
    1. Define path operations for `GET /items/` and `GET /items/{item_id}`.
    1. Define a path operation for `PUT /items/{item_id}` customizing the `tag` and response by using "custom" for the tag and "403" with description "Operation forbidden" respectively.
    1. Make sure to use relative imports to grok them.

1. Populate `app/internal/admin.py` with a simple `POST /update_admin`. The router must be instantiated with the defaults, and the path operation should be established in `/`.

1. Populate your `app/main.py` with:
    1. Instantiate the `FastAPI` app, and configure it with `get_token_query` dependency.
    1. Include the routers from users and items with no further configuration.
    1. Include the router for the admin setting the prefix, to admin, tags to "admin", and dependency with get_token_header. Set the additional responses to 418 "I'm a teapot".


Testing:

+ `GET /`:
    - [ ] Should fail if not including `token` as query parameter
    - [ ] Should be OK when sending query parameter (token=="xxx")

+ `GET /users/`, `GET /users/me`, `GET /users/{username}`
    - [ ] Should fail if not providing `token` query parameter
    - [ ] Should work when sending query parameter

+ `GET /items/`, `GET /items/{item_id}`
    - [ ] Should fail if not providing `token` query parameter and `X-Header` header (token=="xxx" X-Token:"xxx")






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
