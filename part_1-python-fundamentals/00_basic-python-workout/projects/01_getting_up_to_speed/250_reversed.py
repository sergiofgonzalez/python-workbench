"""A practical exercise using reversed()."""

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

    tasks_reversed = list(reversed(tasks))
    print(f"reversed: {tasks_reversed}")
    print(f"original: {tasks}")


if __name__ == "__main__":
    main()
