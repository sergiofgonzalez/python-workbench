"""Illustrate how to use lambdas as arguments to other functions."""

from typing import NamedTuple


class Task(NamedTuple):
    """A simple task with a title, description, and urgency level."""

    title: str
    description: str
    urgency: int


def main() -> None:
    """Application entry point."""
    tasks = [
        Task("Homework", "Physics and math", 5),
        Task("Laundry", "Wash clothes", 3),
        Task("Museum", "Egypt exhibit", 4),
        Task("Toaster", "Clean the toaster", 2),
        Task("Camera", "Export photos", 4),
        Task("Floor", "Mop the floor", 3),
        Task("Internet", "Upgrade plan", 5),
        Task("Utility", "Pay bills", 5),
    ]

    # Sort tasks by urgency, in descending order
    tasks.sort(key=lambda task: task.urgency, reverse=True)
    for task in tasks:
        print(f"{task.title} ({task.urgency}): {task.description}")


if __name__ == "__main__":
    main()
