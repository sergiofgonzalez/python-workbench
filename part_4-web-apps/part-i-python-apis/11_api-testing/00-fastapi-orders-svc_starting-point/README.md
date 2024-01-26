# Orders service using FastAPI
> Starting point for the including tests

## Description

This project implements starting point for the examples of the corresponding chapter, in which testing microservices is explained. The API implemented is documented in the [Orders OpenAPI spec](./oas.yaml), but it is not used for the validation of the service endpoint payloads.


### Setting up shop

The project uses poetry.

As a result, you just need to type:

```bash
$ poetry install
```


To run the project, type:

```bash
poetry run uvicorn orders.app:app --reload --port 8080
```

The endpoints can be tested from the Swagger UI which you can find at http://localhost:8080/docs. Alternatively, you can also go to http://localhost:8080/redoc which is an alternative visualization for REST APIs.

The project also includes HTTPie as a dev dependency for quick testing.