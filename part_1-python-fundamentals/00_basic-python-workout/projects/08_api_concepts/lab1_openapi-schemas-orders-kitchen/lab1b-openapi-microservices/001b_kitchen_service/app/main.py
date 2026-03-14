"""Main application entry point."""

from pathlib import Path

import yaml
from fastapi import FastAPI

from app.routers import kitchen

app = FastAPI()

app.include_router(kitchen.router)


app.openapi_schema = yaml.safe_load(
    (Path(__file__).parent.parent / "openapi_schema_doc.yaml").read_text(),
)
