"""Main application entry point."""

from fastapi import FastAPI

from app.api import orders

app = FastAPI()

app.include_router(orders.router)

