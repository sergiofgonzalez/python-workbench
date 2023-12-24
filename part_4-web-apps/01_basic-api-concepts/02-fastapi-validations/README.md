# Hello, FastAPI Validations
> basic FastAPI + pydantic validations

## Description

This project is an enhancement of [Hello, FastAPI](../01-hello-fastapi/README.md) in which validations are added.

### Setting up shop

The project uses Pipenv for dependency management. The `pipfile` and `pipfile.lock` come from the other project.

In order to start up things you need to:

1. Create and activate a virtualenv
2. Install `pipenv`
2. Run `pipenv install` this will read the `pipfile` and `pipfile.lock` and install the requirements from there.

Validate that it runs doing:

```bash
uvicorn orders.app:app --reload --port 8080
```

The endpoints can be tested from the Swagger UI which you can find at http://localhost:8080/docs. Alternatively, you can also go to http://localhost:8080/redoc which is an alternative visualization for REST APIs.

Those descriptions are not created from the [manually created OpenAPI spec file](oas.yaml), but rather created automatically by FastAPI from our code.