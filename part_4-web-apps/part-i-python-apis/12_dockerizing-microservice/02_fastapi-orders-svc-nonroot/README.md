# An Orders service using FastAPI
> a FastAPI application with powered with CORS, authentication and authorization middleware used for creating a Docker container.

## Description

This project implements a complete microservice for processing orders. It includes a web layer, a data access (repository) and a business layer.

The API implemented is documented in the [Orders OpenAPI spec](./oas.yaml), but Pydantic is used for the validation of the service endpoint payloads (both request and response). The microservice includes a basic authorization layer on the logic to drive logic based on the User ID field that is added to the `request.state` after successful authentication.

Tokens can be generated using [99: Generate JWT](../99_jwt-generator/README.md).

In this step, the third version of the Docker container specification is created (see [Dockerfile](./Dockerfile)). The file is improved using a non-root user.


| NOTE: |
| :---- |
| All the commands below assume you're running outside of poetry's virtualenv and therefore `poetry run` is prefixing all the commands.<br>If you are in shell in which the virtualenv has been activated, you can run the command directly without the `poetry run` prepending it. |


### Setting up shop for non containerized run

The project is a copy of [03: FastAPI Orders service: prj layers](../../06_service-patterns/03-fastapi-orders-svc_prj_layers/) but has been migrated to Poetry.

As a result, to set up shop you need to do:

```bash
poetry install
```

This will create a virtual environment and install the required runtime and development dependencies.

| NOTE: |
| :---- |
| You can get all the details about the virtual environment (e.g., location) by running `poetry env info` . |

#### Building the Docker image


```bash
docker build --build-arg APP_PACKAGE_NAME=orders \
    -t="sergiofgonzalez/orders_svc:0.1.0" .
```

#### Running the Docker image

Run the container in the background (daemon mode) using the default `DB_URL` values which points to the SQLite file `./orders.db` in working dir:

```bash
docker run -d \
    -p 8080:8080 \
    -v $(pwd)/orders.db:/home/monty/app/orders.db  \
    --name orders_svc \
    sergiofgonzalez/orders_svc:0.1.0
```

To override the default `DB_URL` value you can do:

```bash
docker run -d \
    -p 8080:8080 \
    --env DB_URL=sqlite:///orders.db \
    -v $(pwd)/orders.db:/home/monty/app/orders.db  \
    --name orders_svc \
    sergiofgonzalez/orders_svc:0.1.0
```

To run the container in the foreground:

```bash
docker run -it \
    --env DB_URL=sqlite:///orders.db \
    -v $(pwd)/orders.db:/home/monty/app/orders.db  \
    -p 8080:8080 \
    --name orders_svc \
    sergiofgonzalez/orders_svc:0.1.0
```

To open an interactive session within the contain (for inspection), type:

```bash
docker exec -it \
    orders_svc \
    /bin/bash
```

The same image can be run with authentication enabled:

```bash
docker run -d \
    --env AUTH_ON=true \
    -p 8080:8080 \
    -v $(pwd)/orders.db:/home/monty/app/orders.db  \
    --name orders_svc \
    sergiofgonzalez/orders_svc:0.1.0
```

#### Validating the container works as expected

You can test the container using HTTPie:

```bash
$ http localhost:8080/orders order[0][product]=capuccino order[0][size]=small order[0][quantity]:=1 -v
```

```bash
$ http localhost:8080/orders
```

With authorization enabled:

```bash
$ http localhost:8080/orders "Authorization:@token-user1.pem" order[0][product]=machiato order[0][size]=small order[0][quantity]:=1 -v
```

```bash
$ http localhost:8080/orders "Authorization:@token-user1.pem"
```

For additional information, or problems with your DB please review the information below.

#### Prism-cli: mock servers for Kitchen and Payments Services

You'll use `prism-cli` to start up mock servers for the Kitchen and Payments services. This will only require the OpenAPI spec.

In order to start them, you need to run the following commands in separate terminal screens:

```bash
npx @stoplight/prism-cli mock kitchen.yaml --port 3000
```

```bash
npx @stoplight/prism-cli mock payments.yaml --port 3001
```

#### Database

In this step the database was updated. Alembic was complaining so I removed existing versions and ran:

```bash
$ poetry run alembic revision --autogenerate -m "Initial migration with user ID"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'order'
INFO  [alembic.autogenerate.compare] Detected added table 'order_item'
  Generating /home/ubuntu/ ...  done

$ poetry run alembic upgrade heads
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 93b075acb168, Initial migration with user ID
```

#### Starting up the Orders Service

To run the project with authentication enabled, type:

```bash
AUTH_ON=true poetry run uvicorn orders.web.app:app --reload --port 8080
```

The endpoints can be tested from the Swagger UI which you can find at http://localhost:8080/docs/orders.


All the endpoints have been tested and worked mostly OK. There might be a few things that could be slightly improved such as the handling of the filters (i.e., they are sent to the business layer even if not specified as parameters in the query), or the field that is listed as an `int` in the model and should be a UUID string.

#### Testing the authorization layer with HTTPie

The project now also includes HTTPie as one of the dev dependencies. This section describes how to test a few different authorization scenarios. Please note that you will need to generate JWTs to test those.

##### Scenario 1

Create an Order with user ID `ec7bbccf-ca89-4af3-82ac-b41e4831a962`. Then retrieve the list of orders and ensure I'm getting the order I've just created.

```bash
$ http localhost:8080/orders "Authorization: Bearer token" "order[0][product]=capuccino" "order[0][size]=small" "order[0][quantity]:=1" -v
Connection: keep-alive
Content-Length: 69
Content-Type: application/json
Host: localhost:8080
User-Agent: HTTPie/3.2.2

{
    "order": [
        {
            "product": "capuccino",
            "quantity": 1,
            "size": "small"
        }
    ]
}


HTTP/1.1 201 Created
content-length: 165
content-type: application/json
date: Wed, 24 Jan 2024 15:25:10 GMT
server: uvicorn

{
    "created": "2024-01-24T15:09:42.885033",
    "id": "8b3e5b61-c049-4d75-a65b-46afc420811e",
    "order": [
        {
            "product": "capuccino",
            "quantity": 1,
            "size": "small"
        }
    ],
    "status": "created"
}
```

```bash
$ http localhost:8080/orders "Authorization: Bearer token"
HTTP/1.1 200 OK
content-length: 178
content-type: application/json
date: Wed, 24 Jan 2024 15:27:33 GMT
server: uvicorn

{
    "orders": [
        {
            "created": "2024-01-24T15:09:42.885033",
            "id": "8b3e5b61-c049-4d75-a65b-46afc420811e",
            "order": [
                {
                    "product": "capuccino",
                    "quantity": 1,
                    "size": "small"
                }
            ],
            "status": "created"
        }
    ]
}
```

If I use the endpoint to retrieve the specific order ID the user has created it should return OK:

```bash
$ http localhost:8080/orders/8b3e5b61-c049-4d75-a65b-46afc420811e "Authorization:@token-user1.pem"
HTTP/1.1 200 OK
content-length: 165
content-type: application/json
date: Wed, 24 Jan 2024 15:58:41 GMT
server: uvicorn

{
    "created": "2024-01-24T15:09:42.885033",
    "id": "8b3e5b61-c049-4d75-a65b-46afc420811e",
    "order": [
        {
            "product": "capuccino",
            "quantity": 1,
            "size": "small"
        }
    ],
    "status": "created"
}
```

##### Scenario 2

Create a token associated to a new userID `ec7bbccf-ca89-4af3-82ac-b41e4831a999`. Then retrieve the list of orders without having created anything &mdash; the expectation is to get an empty order list:

The file `token-user2.pem` contains `Bearer token-for-user2`.

```bash
$ http localhost:8080/orders "Authorization:@token-user2.pem"
HTTP/1.1 200 OK
content-length: 13
content-type: application/json
date: Wed, 24 Jan 2024 15:35:28 GMT
server: uvicorn

{
    "orders": []
}
```

If I try to get an existing order from another user by ID it should return 404:

```bash
$ http localhost:8080/orders/8b3e5b61-c049-4d75-a65b-46afc420811e "Authorization:@token-user2.pem"
HTTP/1.1 404 Not Found
content-length: 77
content-type: application/json
date: Wed, 24 Jan 2024 15:56:52 GMT
server: uvicorn

{
    "detail": "Order with ID 8b3e5b61-c049-4d75-a65b-46afc420811e was not found"
}
```

