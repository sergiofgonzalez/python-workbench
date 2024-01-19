"""My second Hello, World! FastAPI web app"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/hi/{who}")
def greet(who):
    return f"Hello, {who}!"
