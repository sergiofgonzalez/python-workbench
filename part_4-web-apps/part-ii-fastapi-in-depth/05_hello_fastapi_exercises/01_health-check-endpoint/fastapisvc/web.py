"""FastAPI app"""
from datetime import datetime

from fastapi import FastAPI

app = FastAPI()


@app.get("/health-check")
def health_check() -> dict:
    return {"utc_timestamp": datetime.utcnow(), "status": "OK"}
