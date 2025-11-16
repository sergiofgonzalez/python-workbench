"""Illustrates how to use generic classes for interface checks."""

from collections.abc import Collection
from dataclasses import dataclass


@dataclass
class Task:
    """Represents a task."""

    title: str
    description: str
    urgency: int


def filter_tasks(tasks: list[Task], by_urgency: int | Collection) -> list[Task]:
    """Return the tasks that satisfy the by_urgency filter."""
    if isinstance(by_urgency, int):
        return [task for task in tasks if task.urgency == by_urgency]
    return [task for task in tasks if task.urgency in by_urgency]


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
    # using int
    print(f"{filter_tasks(tasks, 3)=}")
    print("===" * 20)

    # using list
    print(f"{filter_tasks(tasks, [3])=}")
    print("===" * 20)

    print(f"{filter_tasks(tasks, [2, 3])=}")
    print("===" * 20)

    # using tuple
    print(f"{filter_tasks(tasks, (2, 3))=}")
    print("===" * 20)

    # using set
    print(f"{filter_tasks(tasks, {2, 3})=}")
    print("===" * 20)


if __name__ == "__main__":
    main()
