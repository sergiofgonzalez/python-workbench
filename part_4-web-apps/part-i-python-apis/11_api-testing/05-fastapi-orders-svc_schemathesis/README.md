# Orders service using FastAPI
> Step 4 (unittest variant): API Testing with Schemathesis

## Description

This project illustrates how to use Schemathesis to do property-based testing on the APIs.

The API implemented is documented in the [Orders OpenAPI spec](./oas.yaml).


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

### Running the property-based tests schemathesis

To run the basic tests (`not_a_server_error`), type:

```bash
schemathesis run oas_with_links.yaml \
  --base-url=http://localhost:8080 --stateful=links
...
GET /orders .                                     [ 14%]
POST /orders .                                    [ 28%]
    -> GET /orders/{order_id} .                   [ 37%]
    -> PUT /orders/{order_id} .                   [ 44%]
    -> DELETE /orders/{order_id} .                [ 50%]
    -> POST /orders/{order_id}/cancel .           [ 54%]
    -> POST /orders/{order_id}/pay .              [ 58%]
GET /orders/{order_id} .                          [ 66%]
PUT /orders/{order_id} .                          [ 75%]
DELETE /orders/{order_id} .                       [ 83%]
POST /orders/{order_id}/pay .                     [ 91%]
POST /orders/{order_id}/cancel .
...
```

To apply more thorough checks, you can pass the `--checks=all` parameter:

```bash
$ schemathesis run oas_with_links.yaml --base-url=http://localhost:8080 \
  --hypothesis-database=none --stateful=links \
  --checks=all
```

You can also use `--exitfirst` to fail fast in case of problems.

| NOTE: |
| :---- |
| During the initial tests, the `status_code_conformance` checks were failing with 400 when 422 was expected. It was due to incorrect bearer tokens being injected by schemathesis in the invocations of the endpoints. In order to solve them, I had to remove all the security related information from OpenAPI spec that is used by Schemathesis to generate the tests. |
