"""Entrypoint file for FastAPI web server with CORS enabled endpoints"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root() -> dict:
    return {"message": "Hello World!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", reload=True, port=8080)
