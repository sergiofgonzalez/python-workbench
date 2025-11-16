"""Illustrate the use of modern named tuples."""

from typing import NamedTuple

data = """Laundry,Wash clothes,3
Homework,Physics + Math,5
Museum,Egyptian things,2
"""


class Task(NamedTuple):
    """A task with a title, description, and urgency level."""

    title: str
    desc: str
    urgency: int


def main() -> None:
    """Application entry point."""
    # Parse the data into a list of named tuples
    tasks = []
    for line in data.strip().split("\n"):
        title, desc, urgency = line.split(",")
        task = Task(title, desc, int(urgency))
        tasks.append(task)

    print("Tasks (named tuples):", tasks)

    # Accessing fields by name
    for task in tasks:
        print(f"Title: {task.title}, Desc: {task.desc}, Urgency: {task.urgency}")

    # Named tuples are immutable, so you cannot change their values
    try:
        tasks[0].urgency = 4  # type: ignore  # noqa: PGH003
    except AttributeError as err:
        print("Error trying to update a named tuple:", err)


if __name__ == "__main__":
    main()
