"""
Entry point for the web application
"""

import os

from fastapi import FastAPI, Form

app = FastAPI()

@app.get("/who")
def greet(name: str = Form()):
    return f"Hello, {name} on GET!"

@app.post("/who")
def greet2(name: str = Form()):
    return f"Hello, {name} on POST!"

@app.get("/")
def read_root() -> str:
    return "Hello, world!"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=int(os.getenv("PORT", "8080")))
