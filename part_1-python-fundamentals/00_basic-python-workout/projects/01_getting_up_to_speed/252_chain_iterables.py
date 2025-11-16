"""Illustrate how to use chain() to combine multiple iterables."""

from itertools import chain
from typing import NamedTuple


class Task(NamedTuple):
    """A task with a title, description, and urgency level."""

    title: str
    desc: str
    urgency: int


def main() -> None:
    """Application entry point."""
    tasks = [
        Task("Homework", "Physics and math", 5),
        Task("Laundry", "Wash clothes", 3),
        Task("Museum", "Egypt exhibit", 4),
    ]

    completed_tasks = [
        Task("Toaster", "Clean the toaster", 2),
        Task("Camera", "Export photos", 4),
        Task("Floor", "Mop the floor", 3),
    ]

    # combining using list concatenation
    for task in tasks + completed_tasks:
        print(task.title)

    # you can also use chain for a more pythonic approach
    print("===")
    for task in chain(tasks, completed_tasks):
        print(task.title)


if __name__ == "__main__":
    main()
