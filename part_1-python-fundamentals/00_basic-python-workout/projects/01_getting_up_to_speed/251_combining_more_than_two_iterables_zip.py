"""Illustrates how you can use zip() to combine more than two iterables."""

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
    dates = ["May 5, 2022", "May 9, 2022", "May 11, 2022"]
    locations = ["School", "Home", "Downtown"]

    # using zip() to combine the three iterables
    combined = zip(tasks, dates, locations, strict=True)
    for task, date, location in combined:
        print(f"{task.title}: by {date}, at {location}")


if __name__ == "__main__":
    main()
