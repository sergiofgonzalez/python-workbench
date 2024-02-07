"""FastAPI app"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/hi")
def greet(who: str) -> str:
    return f"Hello? {who}?"
