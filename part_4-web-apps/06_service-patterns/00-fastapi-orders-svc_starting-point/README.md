# Implementing an Orders service using FastAPI
> Step 0: Starting point for the chapter

## Description

This project implements starting point for the examples of the corresponding chapter, in which the common microservices patterns are described. The API implemented is documented in the [Orders OpenAPI spec](./oas.yaml), but it is not used for the validation of the service endpoint payloads.


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
