# Hello, FastAPI
> first steps into FastAPI

## Description

This project implements a simple Orders microservice using FastAPI framework that returns hardcoded responses.

It includes an OpenAPI spec file (although it's not being used in runtime).

The project uses Pipenv for dependency management.

For some reason, `pipenv` does not work well for installing virtual environments from scratch. As a workaround, I had to manually create a virtual environment first, then use `pipenv` commands:

```bash
# Create the virtual environment without using pipenv
$ conda run -n base python -m venv .venv --upgrade-deps

# Install FastAPI and uvicorn deps
$ pipenv install fastapi uvicorn
```

Then you can start it using:

```bash
uvicorn orders.app:app --reload --port 8080
```

The endpoints can be tested from the Swagger UI which you can find at http://localhost:8080/docs. Alternatively, you can also go to http://localhost:8080/redoc which is an alternative visualization for REST APIs.

Those descriptions are not created from the [manually created OpenAPI spec file](oas.yaml), but rather created automatically by FastAPI from our code.