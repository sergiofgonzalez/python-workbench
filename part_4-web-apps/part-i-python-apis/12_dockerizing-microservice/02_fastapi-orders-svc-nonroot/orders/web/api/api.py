"""
Orders API layer implementation using FastAPI framework
"""
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from orders.orders_service.exceptions import OrderNotFoundError
from orders.orders_service.orders_service import OrdersService
from orders.repository.orders_repository import OrdersRepository
from orders.repository.unit_of_work import UnitOfWork
from orders.web.api.schemas import (
    CreateOrderSchema,
    GetOrderSchema,
    GetOrdersSchema,
)
from orders.web.app import app


@app.get("/orders", response_model=GetOrdersSchema)
def get_orders(
    request: Request,
    cancelled: Optional[bool] = None,
    limit: Optional[int] = None,
):
    with UnitOfWork() as unit_of_work:
        repo = OrdersRepository(unit_of_work.session)
        orders_service = OrdersService(repo)
        results = orders_service.list_orders(
            cancelled=cancelled, limit=limit, user_id=request.state.user_id
        )
    return {"orders": [result.dict() for result in results]}


@app.post(
    "/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema,
)
def create_order(request: Request, payload: CreateOrderSchema):
    with UnitOfWork() as unit_of_work:
        repo = OrdersRepository(unit_of_work.session)
        orders_service = OrdersService(repo)
        order = payload.model_dump()["order"]
        for item in order:
            item["size"] = item["size"].value
        order = orders_service.place_order(order, request.state.user_id)
        unit_of_work.commit()
        response_payload = order.dict()
    return response_payload


@app.get("/orders/{order_id}", response_model=GetOrderSchema)
def get_order(request: Request, order_id: UUID):
    try:
        with UnitOfWork() as unit_of_work:
            repo = OrdersRepository(unit_of_work.session)
            orders_service = OrdersService(repo)
            order = orders_service.get_order(
                order_id=order_id, user_id=request.state.user_id
            )
        return order.dict()
    except OrderNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} was not found",
        ) from e


@app.put(
    "/orders/{order_id}",
    response_model=GetOrderSchema,
)
def update_order(
    request: Request,
    order_id: UUID,
    order_details: CreateOrderSchema,
):
    try:
        with UnitOfWork() as unit_of_work:
            repo = OrdersRepository(unit_of_work.session)
            orders_service = OrdersService(repo)
            order = order_details.model_dump()["order"]
            for item in order:
                item["size"] = item["size"].value
            order = orders_service.update_order(
                order_id=order_id, user_id=request.state.user_id, items=order
            )
            unit_of_work.commit()
        return order.dict()
    except OrderNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} was not found",
        ) from e


@app.delete("/orders/{order_id}", response_class=Response)
def delete_order(request: Request, order_id: UUID):
    try:
        with UnitOfWork() as unit_of_work:
            repo = OrdersRepository(unit_of_work.session)
            orders_service = OrdersService(repo)
            orders_service.delete_order(
                order_id=order_id, user_id=request.state.user_id
            )
            unit_of_work.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except OrderNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} was not found",
        ) from e


@app.post("/orders/{order_id}/cancel", response_model=GetOrderSchema)
def cancel_order(request: Request, order_id: UUID):
    try:
        with UnitOfWork() as unit_of_work:
            repo = OrdersRepository(unit_of_work.session)
            orders_service = OrdersService(repo)
            order = orders_service.cancel_order(
                order_id=order_id, user_id=request.state.user_id
            )
            unit_of_work.commit()
        return order.dict()
    except OrderNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} was not found",
        ) from e


@app.post("/orders/{order_id}/pay", response_model=GetOrderSchema)
def pay_order(request: Request, order_id: UUID):
    try:
        with UnitOfWork() as unit_of_work:
            repo = OrdersRepository(unit_of_work.session)
            orders_service = OrdersService(repo)
            order = orders_service.pay_order(
                order_id=order_id, user_id=request.state.user_id
            )
            unit_of_work.commit()
        return order.dict()
    except OrderNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} was not found",
        ) from e
