"""My second Hello, World! FastAPI web app"""
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/hi")
def greet(who: str = Header()):
    return f"Hello, {who}!"


@app.get("/agent")
def get_agent(user_agent: str = Header()):
    return f"User-Agent: {user_agent}"
