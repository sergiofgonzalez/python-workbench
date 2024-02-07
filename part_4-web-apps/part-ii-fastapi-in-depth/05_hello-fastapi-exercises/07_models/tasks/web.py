"""FastAPI app"""
from fastapi import Body, FastAPI

from tasks.data import create_one, find_all
from tasks.schema import TaskIn, TaskOut

app = FastAPI()


@app.get("/tasks")
def get_all() -> list[TaskOut]:
    return find_all()  # type: ignore


@app.post("/tasks")
def create(task_in: TaskIn = Body()) -> TaskOut:
    return create_one(task_in)  # type: ignore
