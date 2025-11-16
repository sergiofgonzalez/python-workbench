"""A practical example of breaking early from loops."""

from typing import NamedTuple


class Task(NamedTuple):
    """A task with a title, description, and urgency level."""

    title: str
    desc: str
    urgency: int


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
    for i, task in enumerate(tasks):
        print(f"Checking tasks {i}: {task.title}")
        if task.urgency == 5:  # noqa: PLR2004
            print(f"Urgent task detected: {task}")
            break


if __name__ == "__main__":
    main()
