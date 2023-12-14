from datetime import datetime
from uuid import UUID

from starlette import status
from starlette.responses import Response

from orders.app import app

order = {
    "id": "624f25f2-3d35-4cfc-b710-b64b2ed2942d",
    "status": "delivered",
    "created": datetime.utcnow(),
    "order": [{"product": "capuccino", "size": "medium", "quantity": 1}],
}


@app.get("/orders")
def get_orders():
    return {"orders": [order]}


@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order():
    return order


@app.get("/orders/{order_id}")
def get_order(order_id: UUID):
    return order


@app.put("/orders/{order_id}")
def update_order(order_id: UUID):
    return order


@app.delete("/orders/{order_id}")
def delete_order(order_id: UUID):
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/orders/{order_id}/cancel")
def cancel_order(order_id: UUID):
    return order


@app.post("/orders/{order_id}/pay")
def pay_order(order_id: UUID):
    return order
