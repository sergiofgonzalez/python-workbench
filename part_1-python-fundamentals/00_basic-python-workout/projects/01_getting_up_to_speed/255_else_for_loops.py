"""Illustrate the meaning of else in for loops."""

from typing import NamedTuple


class Task(NamedTuple):
    """A task with a title, description, and urgency level."""

    title: str
    desc: str
    urgency: int


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


def locate_first_task_by_urgency(urgency: int) -> Task | None:
    """Return the first task whose urgency matches the one given."""
    for task in tasks:
        if task.urgency == urgency:
            return task
    else:  # noqa: PLW0120
        return None


def main() -> None:
    """Application entry point."""
    # basic stuff
    for i in range(6):
        print(i)
    else:  # noqa: PLW0120
        print("looping done!")
    print("===")

    # more comprehensive example
    print(f"Found task: {locate_first_task_by_urgency(1)}")
    print(f"Found task: {locate_first_task_by_urgency(4)}")


if __name__ == "__main__":
    main()
