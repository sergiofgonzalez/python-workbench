"""Illustrate how to use `type` to create more generic methods."""

from dataclasses import dataclass


@dataclass
class Task:
    """Represent a task in a to-do list application."""

    title: str
    description: str
    urgency: int


def filter_tasks(tasks: list[Task], by_urgency: int | list[int]) -> list[Task]:
    """Filter tasks by urgency level(s)."""
    if type(by_urgency) is int:
        return [task for task in tasks if task.urgency == by_urgency]
    if type(by_urgency) is list:
        return [task for task in tasks if task.urgency in by_urgency]
    msg = "by_urgency must be an int or a list of ints"
    raise TypeError(msg)


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
    assert filter_tasks(tasks, 3) == [
        Task("Floor", "Mop the floor", 3),
        Task("Laundry", "Wash clothes", 3),
    ]
    assert filter_tasks(tasks, [3, 4, 5]) == [
        Task("Camera", "Export photos", 4),
        Task("Homework", "Physics and math", 5),
        Task("Floor", "Mop the floor", 3),
        Task("Internet", "Upgrade plan", 5),
        Task("Laundry", "Wash clothes", 3),
        Task("Museum", "Egypt exhibit", 4),
        Task("Utility", "Pay bills", 5),
    ]
    print("=== All assertions passed! ===")


if __name__ == "__main__":
    main()
