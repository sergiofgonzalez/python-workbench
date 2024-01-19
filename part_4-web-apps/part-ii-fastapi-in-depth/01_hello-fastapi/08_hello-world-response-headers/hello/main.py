"""My second Hello, World! FastAPI web app"""
from fastapi import FastAPI, Header, Response

app = FastAPI()


@app.get("/hi")
def greet(who: str = Header()):
    return f"Hello, {who}!"


@app.get("/agent")
def get_agent(user_agent: str = Header()):
    return f"User-Agent: {user_agent}"


@app.get("/happy", status_code=202)
def happy():
    return "😀"


@app.get("/header/{name}/{value}")
def header(name: str, value: str, response: Response):
    response.headers[name] = value
    return f"header {name} has been injected!"
