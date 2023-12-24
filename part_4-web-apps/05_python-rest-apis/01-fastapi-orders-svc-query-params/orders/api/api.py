"""Orders API implementation using FastAPI framework
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from fastapi import HTTPException
from starlette import status
from starlette.responses import Response

from orders.api.schemas import (
    CreateOrderSchema,
    GetOrderSchema,
    GetOrdersSchema,
    Status,
)
from orders.app import app

orders = dict()


@app.get("/orders", response_model=GetOrdersSchema)
def get_orders(cancelled: Optional[bool] = None, limit: Optional[int] = None):
    if cancelled is None and limit is None:
        return {"orders": orders.values()}

    query_resultset = orders.values()
    if cancelled is not None:
        if cancelled:
            query_resultset = [
                order
                for order in query_resultset
                if order["status"] == Status.cancelled.value
            ]
        else:
            query_resultset = [
                order
                for order in query_resultset
                if order["status"] != Status.cancelled.value
            ]
    if limit is not None and len(query_resultset) > limit:
        return {"orders": query_resultset[:limit]}

    return {"orders": query_resultset}


@app.post(
    "/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema,
)
def create_order(order_details: CreateOrderSchema):
    order_id = str(uuid4())
    order = {
        "id": order_id,
        "status": Status.created.value,
        "created": datetime.utcnow(),
        "order": order_details.order,
    }
    orders[order_id] = order
    return order


@app.get("/orders/{order_id}", response_model=GetOrderSchema)
def get_order(order_id: UUID):
    if str(order_id) in orders:
        return orders[str(order_id)]
    else:
        # Alternative:
        # return Response(status_code=status.HTTP_404_NOT_FOUND)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} was not found",
        )


@app.put(
    "/orders/{order_id}",
    response_model=GetOrderSchema,
)
def update_order(
    order_id: UUID,
    order_details: CreateOrderSchema,
):
    if str(order_id) not in orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} was not found",
        )

    order = orders[str(order_id)]
    order["order"] = order_details.order
    orders[str(order_id)] = order
    return order


@app.delete("/orders/{order_id}", response_class=Response)
def delete_order(order_id: UUID):
    if str(order_id) in orders:
        del orders[str(order_id)]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/orders/{order_id}/cancel", response_model=GetOrderSchema)
def cancel_order(order_id: UUID):
    if str(order_id) not in orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} was not found",
        )
    orders[str(order_id)]["status"] = Status.cancelled.value
    return orders[str(order_id)]


@app.post("/orders/{order_id}/pay", response_model=GetOrderSchema)
def pay_order(order_id: UUID):
    if str(order_id) not in orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} was not found",
        )
    orders[str(order_id)]["status"] = Status.progress.value
    return orders[str(order_id)]
