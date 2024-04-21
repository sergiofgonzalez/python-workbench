"""
Orders API layer
"""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status

from orders.web.schemas import (
    CreateOrderSchema,
    GetOrderSchema,
    GetOrdersSchema,
    OrderItemSchema,
    Size,
    Status,
)

router = APIRouter(prefix="/orders")


@router.get("")
@router.get("/")
def get_all_orders() -> GetOrdersSchema:
    orders = GetOrdersSchema(
        orders=[
            GetOrderSchema(
                id=uuid4(),
                created=datetime(2021, 1, 1, tzinfo=timezone.utc),
                status=Status.CREATED,
                order=[
                    OrderItemSchema(
                        product="capuccino", size=Size.SMALL, quantity=1
                    )
                ],
            )
        ]
    )
    return orders


@router.get("/{order_id}")
def get_one_order(order_id: UUID) -> GetOrderSchema:
    return GetOrderSchema(
        id=order_id,
        created=datetime(2021, 1, 1, tzinfo=timezone.utc),
        status=Status.CREATED,
        order=[
            OrderItemSchema(product="capuccino", size=Size.SMALL, quantity=1)
        ],
    )


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(order_details: CreateOrderSchema) -> GetOrderSchema:
    return GetOrderSchema(
        id=uuid4(),
        created=datetime.now(timezone.utc),
        status=Status.CREATED,
        order=order_details.order,
    )


@router.put("/{order_id}")
def replace_order(
    order_id: UUID, order_details: CreateOrderSchema
) -> GetOrderSchema:
    return GetOrderSchema(
        id=order_id,
        created=datetime.now(timezone.utc),
        status=Status.CREATED,
        order=order_details.order,
    )


@router.patch("/{order_id}")
def modify_order(order_id: UUID, order_details: dict) -> GetOrderSchema:
    """Raise exception until implemented"""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not (yet) implemented",
    )


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID):
    pass
