"""In-memory task management"""
import uuid
from datetime import datetime
from typing import Dict, Sequence

from pydantic import UUID4

from tasks.schema import Task, TaskIn

_tasks: Dict[UUID4, Task] = dict()


def find_all() -> Sequence[Task]:
    return list(_tasks.values())


def create_one(task_in: TaskIn) -> Task:
    task = Task(
        id=uuid.uuid4(),
        creation_ts=datetime.utcnow(),
        title=task_in.title,
        description=task_in.description,
        urgency=task_in.urgency,
    )
    _tasks[task.id] = task
    return task
