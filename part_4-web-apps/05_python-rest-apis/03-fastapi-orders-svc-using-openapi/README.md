# Implementing an Orders service using FastAPI
> Step 3: Using OpenAPI spec

## Description

This project implements starting point for the examples of the corresponding chapter. The API implemented is described by the [Orders OpenAPI spec](./oas.yaml).


In this step, we ban undeclared properties.

### Setting up shop

The project uses venv for virtual environment management and pip for dependency management.

As a result, you just need to:

```bash
$ conda run -n web python -m venv .venv --upgrade-deps
$ source .venv/bin/activate
$ pip install -r requirements.txt
```


To run the project, type:

```bash
uvicorn orders.app:app --reload --port 8080
```

The endpoints can be tested from the Swagger UI which you can find at http://localhost:8080/docs. Alternatively, you can also go to http://localhost:8080/redoc which is an alternative visualization for REST APIs.


Note that the Swagger endpoints are not created from the [manually created OpenAPI spec file](oas.yaml), but rather created automatically by FastAPI from the code.

## Sample Payloads