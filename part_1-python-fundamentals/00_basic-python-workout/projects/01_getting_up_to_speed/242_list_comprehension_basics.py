"""A simple application of list comprehensions."""

from typing import NamedTuple


class Task(NamedTuple):
    """A task with a title, description, and urgency level."""

    title: str
    description: str
    urgency: int


def main() -> None:
    """Application entry point."""
    # Part 1: create a list of squares of numbers from 1 to 4
    squares = [x**2 for x in range(1, 5)]
    print(squares)
    assert squares == [1, 4, 9, 16]
    print("=== Part 1 passed ===")

    # Part 2: create a list of Tasks
    tasks = [
        Task("Homework", "Physics and math", 5),
        Task("Laundry", "Wash clothes", 3),
        Task("Museum", "Egypt exhibit", 4),
    ]

    titles = [task.title for task in tasks]
    print(titles)
    assert titles == ["Homework", "Laundry", "Museum"]

    # Now using map() instead of list comprehension
    # in map() the first argument is the mapping function, the 2nd is the iterable
    titles_map = list(map(lambda task: task.title, tasks))  # noqa: C417
    print(titles_map)
    assert titles_map == ["Homework", "Laundry", "Museum"]

    print("=== Part 2 passed ===")


if __name__ == "__main__":
    main()
