# Orders service with Postgres using an image from ACR
> The orders service with Postgres as db engine referencing the orders_svc image from ACR

| NOTE: |
| :---- |
| The commands assume the ACR registry name `acrname`. |

As a prerequisite, the Docker image for the service needs to be available in Azure Container Registry (ACR) as `acrname.azurecr.io/coffeemesh/orders_svc:latest` (see [Publishing Orders Service to ACR](../03_fastapi-orders-svc-docker-compose/README.md#publish-to-azure-container-registry-acr).)

If the image is available, you just need to type the following command in the working directory:

```bash
# ACR login (if needed)
docker login acrname.azurecr.io

# Run the services in docker-compose.yaml
docker compose up
```

That command will build the images (if needed), create the internal network, and run the containers.

#### Populating the PostgreSQL tables

Before testing the application, you need to populate the Postgres schema. This can be done running the Alembic command in the `03_fastapi-orders-svc-docker-compose/` directory:

```bash
$ cd ../03_fastapi-orders-svc-docker-compose

$ DB_URL=postgresql://postgres:postgres@localhost:5432/postgres poetry \
  run alembic upgrade heads
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 0e8aed7229af, Fix incorrect order_id type
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

In this step the database was updated. Alembic was complaining so I removed existing version files under `./migrations/versions/` and ran:

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

