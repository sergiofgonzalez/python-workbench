"""FastAPI app"""
from fastapi import Body, FastAPI

app = FastAPI()


@app.get("/hi")
def greet(who: str = Body(embed=True)) -> str:
    return f"Hello? {who}?"
