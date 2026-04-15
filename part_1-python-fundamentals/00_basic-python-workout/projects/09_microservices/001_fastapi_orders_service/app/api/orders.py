"""Greeter router: contains all path operations related to greetings."""

from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, Query, status

from app.api.schemas import (
    CreateOrderSchema,
    GetOrderSchema,
    GetOrdersSchema,
    ReadOrdersQueryParams,
    StatusEnum,
)

router = APIRouter(prefix="/orders", tags=["orders"])

fake_orders_db = {}


@router.get("/")
async def read_orders(
    query_params: Annotated[ReadOrdersQueryParams, Query()],
) -> GetOrdersSchema:
    """Get a list of all orders."""
    orders = list(fake_orders_db.values())
    if query_params.cancelled:
        orders = [order for order in orders if order["status"] == StatusEnum.CANCELLED]
    elif query_params.cancelled is False:
        orders = [order for order in orders if order["status"] != StatusEnum.CANCELLED]
    if query_params.limit is not None:
        orders = orders[: query_params.limit]
    return GetOrdersSchema(orders=list(orders))


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order: CreateOrderSchema) -> GetOrderSchema:
    """Create a new order."""
    new_order = GetOrderSchema(
        order_id=uuid4(),
        created=datetime.now(UTC),
        status=StatusEnum.CREATED,
        order=order.order,
    )
    fake_orders_db[new_order.order_id] = new_order.model_dump()
    return new_order


@router.get("/{order_id}")
async def read_order(order_id: UUID) -> GetOrderSchema:
    """Get a single order by ID."""
    order = fake_orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return GetOrderSchema(**order)


@router.put("/{order_id}")
async def update_order_status(
    order_id: UUID,
    order_update: CreateOrderSchema,
) -> GetOrderSchema:
    """Update the content of an order."""
    order = fake_orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    fake_orders_db[order_id] = GetOrderSchema(
        order_id=order_id,
        created=order["created"],
        status=order["status"],
        order=order_update.order,
    ).model_dump()
    return GetOrderSchema(**fake_orders_db[order_id])


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: UUID) -> None:
    """Delete an order by ID."""
    if order_id not in fake_orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    del fake_orders_db[order_id]


@router.post("/{order_id}/cancel")
async def cancel_order(order_id: UUID) -> GetOrderSchema:
    """Cancel an order by ID."""
    order = fake_orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    fake_orders_db[order_id] = GetOrderSchema(
        order_id=order_id,
        created=order["created"],
        status=StatusEnum.CANCELLED,
        order=order["order"],
    ).model_dump()
    return GetOrderSchema(**fake_orders_db[order_id])


@router.post("/{order_id}/pay")
async def pay_order(order_id: UUID) -> GetOrderSchema:
    """Pay for an order by ID."""
    order = fake_orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    fake_orders_db[order_id] = GetOrderSchema(
        order_id=order_id,
        created=order["created"],
        status=StatusEnum.IN_PROGRESS,
        order=order["order"],
    ).model_dump()
    return GetOrderSchema(**fake_orders_db[order_id])
