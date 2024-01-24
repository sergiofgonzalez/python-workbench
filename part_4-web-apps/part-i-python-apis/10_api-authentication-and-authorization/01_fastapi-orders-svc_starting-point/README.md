# An Orders service using FastAPI
> empty starting point to add authentication and authorization to a FastAPI application.

## Description

This project implements a complete microservice for processing orders. It includes a web layer, a data access (repository) and a business layer.

The API implemented is documented in the [Orders OpenAPI spec](./oas.yaml), but Pydantic is used for the validation of the service endpoint payloads (both request and response).

This project represents an empty starting point (i.e., you need to go through the setup steps).

| NOTE: |
| :---- |
| All the commands below assume you're running outside of poetry's virtualenv and therefore `poetry run` is prefixing all the commands.<br>If you are in shell in which the virtualenv has been activated, you can run the command directly without the `poetry run` prepending it. |


### Setting up shop

The project is a copy of [03: FastAPI Orders service: prj layers](../../06_service-patterns/03-fastapi-orders-svc_prj_layers/) but has been migrated to Poetry.

As a result, to set up shop you need to do:

```bash
poetry install
```

This will create a virtual environment and install the required runtime and development dependencies.

| NOTE: |
| :---- |
| You can get all the details about the virtual environment (e.g., location) by running `poetry env info` . |


#### Prism-cli: mock servers for Kitchen and Payments Services

You'll use `prism-cli` to start up mock servers for the Kitchen and Payments services. This will only require the OpenAPI spec.

In order to start them, you need to run the following commands in separate terminal screens:

```bash
npx @stoplight/prism-cli mock kitchen.yaml --port 3000
```

```bash
npx @stoplight/prism-cli mock payments.yaml --port 3001
```

#### Starting up the Orders Service

To run the project, type:

```bash
poetry run uvicorn orders.web.app:app --reload --port 8080
```

The endpoints can be tested from the Swagger UI which you can find at http://localhost:8080/docs/orders.


All the endpoints have been tested and worked mostly OK. There might be a few things that could be slightly improved such as the handling of the filters (i.e., they are sent to the business layer even if not specified as parameters in the query), or the field that is listed as an `int` in the model and should be a UUID string.

The project now also includes HTTPie.