from datetime import datetime
from uuid import UUID

from starlette import status
from starlette.responses import Response

from orders.api.schemas import (
    CreateOrderSchema,
    GetOrderSchema,
    GetOrdersSchema,
)
from orders.app import app

order = {
    "id": "624f25f2-3d35-4cfc-b710-b64b2ed2942d",
    "status": "delivered",
    "created": "datetime.utcnow()",
    "updated": datetime.utcnow(),   # Will be filtered out from the response
    "order": [{"product": "capuccino", "size": "medium", "quantity": 2}],
}


@app.get("/orders", response_model=GetOrdersSchema)
def get_orders():
    return {"orders": [order]}


@app.post(
    "/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema,
)
def create_order(order_details: CreateOrderSchema):
    return order


@app.get("/orders/{order_id}", response_model=GetOrderSchema)
def get_order(order_id: UUID):
    return order


@app.put(
    "/orders/{order_id}",
    response_model=GetOrderSchema,
)
def update_order(
    order_id: UUID,
    order_details: CreateOrderSchema,
):
    return order


@app.delete("/orders/{order_id}", response_class=Response)
def delete_order(order_id: UUID):
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/orders/{order_id}/cancel", response_model=GetOrderSchema)
def cancel_order(order_id: UUID):
    return order


@app.post("/orders/{order_id}/pay", response_model=GetOrderSchema)
def pay_order(order_id: UUID):
    return order
