# 001: FastAPI in-memory order management app
> Basic in-memory, fake DB, order management application that returns non-hardcoded responses.

## Project description

Very basic in-memory order management is implemented to be able to respond non-hardcoded responses by using a fake DB (implemented as a dictionary).

In this lab, the models that are used in the path operations reflect what each of the operations require (i.e., no effort spent trying to use inheritance).


### Application specs

1. Set up the structure of the "bigger application" with an `app` and `routers` sub-package to define the APIs.

1. Create the following files within the `routers` subpackage:
    + `orders.py`: to host your path operations and fake db.
    + `schemas.py`: to host your Pydantic models.

1. Create the following Pydantic models in `schemas.py` according to the following specs:
    + `OrderItemSchema`: represents an item within your order.
        + `product`: required str
        + `size`: enumeration accepting "small", "medium", and "big" values.
        + `quantity`: optional int, default value=1, must be >= 1.

    + `CreateOrderSchema`: represents an order as a list of items.
        + `order`: required list of `OrderItemSchema`, min length should be 1.

    + `GetOrderSchema`: represents your order once accepted by the system with additional metadata
        + `id`: required UUID
        + `created`: required timestamp
        + `status`: required enumeration accepting the values "created", "progress", "cancelled", "dispatched", "delivered".
        + `items`: list of items within your order.

    + `GetOrdersSchema`: represents the list of orders in the system.
        + `orders`: required list of `GetOrderSchema`

1. Create the following path operations in your `orders.py` module:

    1. Before anything, create a `fake_orders_db` as an empty dictionary.
    1. Instantiate your router app.
    1. Create the path operation for the `GET /orders/` endpoint. It must return `GetOrdersSchema` instances, and the shape of the response must be like the following:

        ```json
        {
            "orders": [order1, order2, ...]
        }
        ```

    1. Create the path operation for the `POST /orders/` endpoint. It must accept a body with a `CreateOrderSchema` instances, and within the path operation you should add it to the fake db of orders and return a `GetOrderSchema` model. Besides, the path operation must return a 201 upon successful creation.

    1. Create the path operation for the `GET /orders/{order_id}` endpoint. The coroutine must receive the `order_id` as a request parameter and should return a `GetOrderSchema`. If the given `order_id` is not found in the fake DB, a 404 with detail "Order not found" must be returned.

    1. Create the path operation for `PUT /orders/{order_id}`. The path operation must receive the `order_id` and an instance of `CreateOrderSchema` (no partial updates). Within the coroutine, you must return a 404 if the given id is not found in the DB, and if found, you should replace the existing order by the given one. The updated order should be returned (an instance of `GetOrderSchema`).

    1. Create a path operation for `DELETE /orders/{order_id}` which returns a 404 if the given id was not found, and a 204 if the id was successfully removed from the fake db.

    1. Create a path operation for `POST /orders/{order_id}/cancel`. In the path operation, you should update the status of the order to cancelled if the given id is found in the fake db. Otherwise, a 404 should be returned.

    1. Create a path operation for `POST /orders/{order_id}/pay`. In the path operation, you should update the status of the order to in progress if the given id is found in the fake db. Otherwise, a 404 should be returned.



## Running the program

You can run the application with:

```bash
uv run fastapi dev main.py --port {port}
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

The only other dependency was ruff:

```bash
$ uv add ruff --dev
```
