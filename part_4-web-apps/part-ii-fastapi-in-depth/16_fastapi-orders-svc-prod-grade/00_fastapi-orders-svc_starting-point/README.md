# FastAPI: Production grade Orders Service
> Starting point

## Description

In this version I just make sure that the old version Orders service works using Poetry. Authorization and unit tests are removed.
Custom OpenAPI spec has been preserved.

## Setting up shop

The project uses Poetry. To start the server do:

```bash
$ poetry install
$ DB_URL="sqlite:///orders.db" alembic upgrade heads
$ DB_URL="sqlite:///orders.db" poetry run uvicorn orders.web.app:app --port 8080 --reload
```

## Testing the application

At this stage there is no unit, integration or end-to-end tests, but you can test the application with HTTPie or your browser using Swagger.

### Shakedown using HTTPie

```bash
$ http localhost:8080/orders order[0][product]=capuccino order[0][size]=small order[0][quantity]:=1 -v
```

```bash
$ http localhost:8080/orders
```