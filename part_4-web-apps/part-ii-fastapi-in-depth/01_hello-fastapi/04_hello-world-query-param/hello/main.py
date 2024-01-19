"""My second Hello, World! FastAPI web app"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/hi")
def greet(who):
    if who is None:
        who = "stranger"
    return f"Hello, {who}!"
