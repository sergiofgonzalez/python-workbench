"""My second Hello, World! FastAPI web app"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/hi")
def greet():
    return "Hello, world!"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("hello.main:app", reload=True, port=8080)
