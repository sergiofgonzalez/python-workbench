"""My second Hello, World! FastAPI web app"""
from fastapi import FastAPI, Header, Response
from fastapi.responses import HTMLResponse, PlainTextResponse

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


@app.get("/plain", response_class=PlainTextResponse)
def plain_response():
    return "Hello!"


@app.get("/html", response_class=HTMLResponse)
def html_response():
    return """
        <!doctype html>
        <head>
            <title>Hello, html!</title>
        </head>
        <body>
            <h1>Hello, html!</h1>
        </body>
        </html>
        """


@app.get("/xml")
def xml_response():
    data = """<?xml version="1.0"?>
    <person>
        <name>Jason</name>
        <surname>Isaacs</surname>
    </person>
    """
    return Response(content=data, media_type="application/xml")
