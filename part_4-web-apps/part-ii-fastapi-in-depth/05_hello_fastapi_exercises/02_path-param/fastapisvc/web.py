"""FastAPI app"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/hi/{who}")
def greet(who: str) -> str:
    return f"Hello? {who}?"
