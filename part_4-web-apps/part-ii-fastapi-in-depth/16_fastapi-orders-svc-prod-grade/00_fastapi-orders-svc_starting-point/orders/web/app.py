"""FastAPI app entrypoint"""

from pathlib import Path

import yaml
from fastapi import FastAPI

app = FastAPI(
    debug=True, openapi_url="/openapi/orders.json", docs_url="/docs/orders"
)

app.openapi = lambda: oas_doc
oas_doc = yaml.safe_load((Path(__file__).parent / "../../oas.yaml").read_text())


from orders.web.api import api
