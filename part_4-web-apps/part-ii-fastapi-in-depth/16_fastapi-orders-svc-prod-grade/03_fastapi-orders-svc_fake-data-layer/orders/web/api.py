"""
Orders API layer
"""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status

from orders.models.web_models import (
    CreateOrderSchema,
    GetOrderSchema,
    GetOrdersSchema,
    OrderItemSchema,
    Size,
    Status,
)
from orders.repository.orders_repository import OrdersRepository
from orders.repository.unit_of_work import UnitOfWork
from orders.service.exceptions import OrderNotFoundError
from orders.service.orders import OrdersService

router = APIRouter(prefix="/orders")


# Duplicating decorators for empty and "/" paths:
# see https://github.com/tiangolo/fastapi/discussions/7298 for further info
@router.get("/", response_model=GetOrdersSchema)
@router.get("", response_model=GetOrdersSchema, include_in_schema=False)
def get_all_orders(
    cancelled: bool | None = None, limit: int | None = None
) -> dict:
    with UnitOfWork() as unit_of_work:
        repo = OrdersRepository(unit_of_work.session)
        orders_service = OrdersService(repo)
        orders = orders_service.list_orders(
            cancelled=cancelled, limit=limit, user_id="guest"
        )
    return {"orders": [result.dict() for result in orders]}


@router.get("/{order_id}", response_model=GetOrderSchema)
def get_one_order(order_id: UUID) -> dict:
    try:
        with UnitOfWork() as unit_of_work:
            repo = OrdersRepository(unit_of_work.session)
            orders_service = OrdersService(repo)
            order = orders_service.get_order(order_id=order_id, user_id="guest")
        return order.dict()
    except OrderNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e


# Duplicating decorators for empty and "/" paths:
# see https://github.com/tiangolo/fastapi/discussions/7298 for further info
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=GetOrderSchema
)
@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema,
    include_in_schema=False,
)
def create_order(payload: CreateOrderSchema) -> dict:
    with UnitOfWork() as unit_of_work:
        repo = OrdersRepository(unit_of_work.session)
        orders_service = OrdersService(repo)
        order = payload.model_dump()["order"]
        for item in order:
            # Convert the size from a Size enum to a string for the db model
            item["size"] = item["size"].value
        new_order = orders_service.place_order(items=order, user_id="guest")
        unit_of_work.commit()
        response_payload = new_order.dict()
    return response_payload


@router.put("/{order_id}", response_model=GetOrderSchema)
def replace_order(order_id: UUID, payload: CreateOrderSchema) -> dict:
    try:
        with UnitOfWork() as unit_of_work:
            repo = OrdersRepository(unit_of_work.session)
            orders_service = OrdersService(repo)
            order = payload.model_dump()["order"]
            for item in order:
                # Convert the size from a Size enum to a string for the db model
                item["size"] = item["size"].value
            updated_order = orders_service.update_order(
                order_id=order_id, user_id="guest", items=order
            )
            unit_of_work.commit()
        return updated_order.dict()
    except OrderNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID) -> None:
    try:
        with UnitOfWork() as unit_of_work:
            repo = OrdersRepository(unit_of_work.session)
            orders_service = OrdersService(repo)
            orders_service.delete_order(order_id=order_id, user_id="guest")
            unit_of_work.commit()
    except OrderNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
