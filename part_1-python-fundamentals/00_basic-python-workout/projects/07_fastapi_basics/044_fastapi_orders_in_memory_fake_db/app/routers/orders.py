"""Orders router: contains all path operations related to orders."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status

from app.routers.schemas import (
    CreateOrderSchema,
    GetOrderSchema,
    GetOrdersSchema,
    StatusEnum,
)

router = APIRouter(prefix="/orders", tags=["orders"])

fake_orders_db = {}


@router.get("/")
async def read_orders() -> GetOrdersSchema:
    """Get all orders."""
    return GetOrdersSchema(orders=list(fake_orders_db.values()))


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order: CreateOrderSchema) -> GetOrderSchema:
    """Create a new order."""
    new_order = GetOrderSchema(
        id=uuid4(),
        created=datetime.now(UTC),
        status=StatusEnum.CREATED,
        items=order.items,
    )
    new_order_dict = new_order.model_dump()
    fake_orders_db[new_order.id] = new_order_dict
    return new_order


@router.get("/{order_id}")
async def read_order(order_id: UUID) -> GetOrderSchema:
    """Get an order by ID."""
    order = fake_orders_db.get(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return GetOrderSchema(**order)


@router.put("/{order_id}")
async def update_order(order_id: UUID, order: CreateOrderSchema) -> GetOrderSchema:
    """Update an existing order."""
    order_db = fake_orders_db.get(order_id)
    if not order_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    updated_order = GetOrderSchema(
        id=order_id,
        created=order_db["created"],
        status=order_db["status"],
        items=order.items,
    )
    fake_orders_db[order_id] = updated_order.model_dump()
    return updated_order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: UUID) -> None:
    """Delete an order by ID."""
    if order_id not in fake_orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    del fake_orders_db[order_id]


@router.post("/{order_id}/cancel")
async def cancel_order(order_id: UUID) -> GetOrderSchema:
    """Cancel an order by ID."""
    order_db = fake_orders_db.get(order_id)
    if not order_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    if order_db["status"] in [
        StatusEnum.CANCELLED,
        StatusEnum.DISPATCHED,
        StatusEnum.DELIVERED,
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order in status '{order_db['status']}' cannot be cancelled",
        )
    order_db["status"] = StatusEnum.CANCELLED
    fake_orders_db[order_id] = order_db
    return GetOrderSchema(**order_db)


@router.post("/{order_id}/pay")
async def pay_order(order_id: UUID) -> GetOrderSchema:
    """Pay for an order by ID."""
    order_db = fake_orders_db.get(order_id)
    if not order_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    if order_db["status"] != StatusEnum.CREATED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only orders in 'created' status can be paid for",
        )
    order_db["status"] = StatusEnum.PROGRESS
    fake_orders_db[order_id] = order_db
    return GetOrderSchema(**order_db)
