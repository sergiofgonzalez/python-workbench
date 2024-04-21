"""Entrypoint file for FastAPI Orders microservice"""

import os

from fastapi import FastAPI
from orders.web import api as orders_api

app = FastAPI()
app.include_router(orders_api.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=int(os.getenv("PORT", "8080")))
