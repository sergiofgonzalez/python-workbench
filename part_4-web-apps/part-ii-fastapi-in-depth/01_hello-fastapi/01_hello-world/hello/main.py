"""My first Hello, World! FastAPI web app"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/hi")
def greet():
    return "Hello, world!"
