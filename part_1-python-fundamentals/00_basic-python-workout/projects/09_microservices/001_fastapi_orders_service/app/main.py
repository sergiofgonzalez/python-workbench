"""Main application entry point."""

import yaml
from fastapi import FastAPI
from fastapi.responses import Response

from app.api import orders

app = FastAPI()

app.include_router(orders.router)


@app.get("/openapi.yaml", include_in_schema=False)
async def openapi_yaml() -> Response:
    """Return the OpenAPI schema as formatted YAML."""
    schema = app.openapi()
    yaml_content = yaml.safe_dump(schema, default_flow_style=False, sort_keys=False)
    return Response(content=yaml_content, media_type="application/yaml")
