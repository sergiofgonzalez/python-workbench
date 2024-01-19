"""My second Hello, World! FastAPI web app"""
from fastapi import FastAPI, Body

app = FastAPI()


@app.post("/hi")
def greet(who: str = Body(embed=True)):
    return f"Hello, {who}!"
