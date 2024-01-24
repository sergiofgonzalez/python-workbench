# An Orders service using FastAPI
> adding authentication and authorization to a FastAPI application.

## Description

This project implements a complete microservice for processing orders. It includes a web layer, a data access (repository) and a business layer.

The API implemented is documented in the [Orders OpenAPI spec](./oas.yaml), but Pydantic is used for the validation of the service endpoint payloads (both request and response).

This project adds a JWT based authentication layer to the endpoints using authentication middleware. The tokens can be generated using [03: Generate JWT](../03_jwt-generator/README.md)

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

#### Testing the authorization layer with HTTPie

The project now also includes HTTPie as one of the dev dependencies. This section describes how to test the different authentication scenarios.

##### Checking the `AUTH_ON` feature flag

If `AUTH_ON` environment variable is not defined or not present, requests should go through unauthenticated.

1. Start the project without `AUTH_ON`:

    ```bash
    $ poetry run uvicorn orders.web.app:app --port 8080 --reload
    ```

2. Send an unauthenticated request to `/orders`. It should return with a 200.

    ```bash
    $ http localhost:8080/orders
    HTTP/1.1 200 OK
    content-length: 13
    content-type: application/json
    date: Wed, 24 Jan 2024 08:29:16 GMT
    server: uvicorn

    {
        "orders": []
    }
    ```

3. Start the project with `AUTH_ON` set to False. Unauthenticated requests should go through as well.

    ```bash
    AUTH_ON=false poetry run uvicorn orders.web.app:app --port 8080 --reload
    ```

4. Start the project with `AUTH_ON` set to "True". It should fail with 401.

    ```bash
    AUTH_ON=true poetry run uvicorn orders.web.app:app --port 8080 --reload
    ```

##### Checking authentication scenarios

With the server started with `AUTH_ON=true` run the following tests.

You can generate tokens with the [03: Generate JWT](../03_jwt-generator/) project.

- [X] Request with no `Authorization` header fails
- [X] Request with `Authorization: Basic user:pass` fails
- [X] Request with `Authorization: Bearer ` fails
- [X] Request with `Authorization: Bearer <random string>` fails
- [X] Request with `Authorization: Bearer valid but expired token` fails
- [X] Request with `Authorization: Bearer valid but unexpected audience token` fails
- [X] Request with `Authorization: Bearer valid but made up signature` fails
- [X] Request with `Authorization: Bearer valid token` passes through

##### Checking access to public endpoints

Point your browser to http://localhost:8080/docs/orders and http://localhost:8080/openapi/orders.json. Both should work without authentication.

They should work with authentication too.