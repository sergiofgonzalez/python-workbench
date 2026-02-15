"""{{cookiecutter.project_description}}."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root() -> dict[str, str]:
    """Path operation for the GET root endpoint."""
    return {"message": "Hello, world!"}
