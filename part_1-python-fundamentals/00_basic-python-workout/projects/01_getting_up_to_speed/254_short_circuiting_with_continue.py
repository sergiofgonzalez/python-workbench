"""A practical example of short-circuiting with continue."""

from typing import NamedTuple


class Task(NamedTuple):
    """A task with a title, description, and urgency level."""

    title: str
    desc: str
    urgency: int


def print_urgent_task(task: Task) -> None:
    """Print the urgent task details."""
    print(f"Important/Urgent task: {task}")


def main() -> None:
    """Application entry point."""
    tasks = [
        Task("Toaster", "Clean the toaster", 2),
        Task("Camera", "Export photos", 4),
        Task("Homework", "Physics and math", 5),
        Task("Floor", "Mop the floor", 3),
        Task("Internet", "Upgrade plan", 5),
        Task("Laundry", "Wash clothes", 3),
        Task("Museum", "Egypt exhibit", 4),
        Task("Utility", "Pay bills", 5),
    ]
    for task in tasks:
        if task.urgency < 4:  # noqa: PLR2004
            continue
        print_urgent_task(task)


if __name__ == "__main__":
    main()
