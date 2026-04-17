# 001: FastAPI Orders Service with DB models
> Starting point for simple microservice with DB models

## Project description

Starting point for the Orders service which will eventually feature SQLAlchemy DB models and a SQLite backed DB.

The microservice exposes the endpoints listed below, and the service logic is very simple (e.g., a cancelled order can be paid).

The project structure has been adapted to conform to FastAPI recommendations and conventions:

+ The main package is called `app` so that `fastapi` command autodiscovers it.
+ No need to create an intermediate `app.web` package for the path operations.
+ While `routers` is FastAPI recommendation, `api` is more generic.



### Sample requests

+ Create an order:

```bash
$ http post :5000/orders/ \
  order[0][product]=nostra \
  order[0][size]=medium \
  order[0][quantity]=2 \
  order[1][product]="frutti di mare" \
  order[1][size]=large \
  order[2][product]="calzone di nutella" \
  order[2][size]=small
```

+ Read orders:

    + Read all orders:

    ```bash
    $ http :5000/orders/
    ```

    + Read cancelled orders:

    ```bash
    $ http :5000/orders/ cancelled==true
    ```

    + Read up to n (n>=1) orders:

    ```bash
    $ http :5000/orders/ limit==10
    ```

+ Read an order:

```bash
$ http :5000/orders/91ddba36-c213-4374-9da6-5d6a31960cff
```

+ Update an order:

    The product and sizer of the third item in the order is changed.


```bash
$ http put :5000/orders/ \
  order[0][product]=nostra \
  order[0][size]=medium \
  order[0][quantity]=2 \
  order[1][product]="frutti di mare" \
  order[1][size]=large \
  order[2][product]="tiramisu di nutella" \
  order[2][size]=large
```

+ Delete an order:

    ```bash
    http delete :5000/orders/91ddba36-c213-4374-9da6-5d6a31960cff
    ```


+ Cancel an order:

    ```bash
    $ http post :5000/orders/c21c227a-ab30-4d9e-81f4-a7121737c44b/cancel
    ```

+ Pay for an order:

    ```bash
    $ http post :5000/orders/c21c227a-ab30-4d9e-81f4-a7121737c44b/pay
    ```

## Running the program

You can run the application with:

```bash
uv run fastapi dev --port {port}
```

## Running your tests

You can run the tests from your IDE or from the command line using:

```bash
uv run pytest
```

## Project management

This project is managed using `uv`.

FastAPI dependency was added using:

```bash
$ uv add fastapi[standard-no-fastapi-cloud-cli]
```

as I don't intend to use FastAPI cloud at the moment.

PyTest (+ `pytest-sugar` + `pytest-cov`) and Ruff were also added as dev dependencies:

```bash
$ uv add fastapi[standard-no-fastapi-cloud-cli] --dev
```

## Claude Code details

This repository has been co-created with Claude Code.

While the code has been crafted manually for learning purposes, the tests have been created by Claude Code.

Additionally, the playwright MCP server has been added using:

```bash
$ claude mcp add playwright npx @playwright/mcp@latest
```

You can validate that the mcp server has been effectively added by running `/mcp` within Claude Code and making sure it's connected.

With the MCP Playwright server in place, you can do complicated things like the following:

```
Using the Playwright MCP server, go to the Swagger UI and run the same tests available in @tests/unit/test_orders.py from Swagger UI, creating an easy to read markdown file showing the results.
```