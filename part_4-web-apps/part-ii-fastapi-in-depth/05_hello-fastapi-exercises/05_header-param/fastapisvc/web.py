"""FastAPI app"""
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/hi")
def greet(who: str = Header()) -> str:
    return f"Hello? {who}?"
