"""Main application entry point."""

from pathlib import Path

import yaml
from fastapi import FastAPI

from app.routers import orders

app = FastAPI()

app.include_router(orders.router)

openapi_schema_doc = yaml.safe_load(
    (Path(__file__).parent.parent / "openapi_schema_doc.yaml").read_text(),
)

app.openapi_schema = openapi_schema_doc
