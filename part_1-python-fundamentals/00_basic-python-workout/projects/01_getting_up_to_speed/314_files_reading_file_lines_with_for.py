"""Illustrate reading file lines with a for loop."""

from collections.abc import Iterable
from pathlib import Path
from typing import NamedTuple

tasks_file_path = Path("data/in_data/tasks/tasks.csv")


class Task(NamedTuple):
    """Represent a task with id, title, and urgency."""

    id: int
    title: str
    urgency: int


def main() -> None:
    """Application entry point."""
    tasks: list[Task] = []

    with tasks_file_path.open() as file:
        print(f"{isinstance(file, Iterable)=}")

        for line in file:
            parts: Iterable[str] = line.split(",")
            task_id_str, task_name, task_urgency_str = parts

            task = Task(
                id=int(task_id_str),
                title=task_name,
                urgency=int(task_urgency_str),
            )
            tasks.append(task)

    print(tasks)


if __name__ == "__main__":
    main()
