import os

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def top():
    return "root of the web layer here"


@app.get("/echo/{msg}")
def echo(msg):
    return f"echo: {msg}"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app",  reload=True, port=os.getenv("PORT", 8080))
