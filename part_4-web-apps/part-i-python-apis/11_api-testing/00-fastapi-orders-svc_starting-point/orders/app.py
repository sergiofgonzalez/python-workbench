"""FastAPI app entrypoint"""
from pathlib import Path

import yaml
from fastapi import FastAPI

app = FastAPI(debug=True)

oas_doc = yaml.safe_load((Path(__file__).parent / "../oas.yaml").read_text())

app.openapi = lambda: oas_doc

from orders.api import api
