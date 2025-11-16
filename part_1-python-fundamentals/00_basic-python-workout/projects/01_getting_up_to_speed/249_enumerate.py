"""A practical example of enumerate."""

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
    for i, task in enumerate(tasks):
        print(f"Task {i + 1}: {task.title:10}{task.desc:20}{task.urgency:2}")


if __name__ == "__main__":
    main()
