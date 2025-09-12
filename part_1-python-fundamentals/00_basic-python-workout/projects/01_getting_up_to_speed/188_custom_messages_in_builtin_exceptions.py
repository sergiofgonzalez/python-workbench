"""Illustrates how to use custom messages in built-in exceptions."""

from typing import NamedTuple


class Task(NamedTuple):
    """Represents a task with a title and urgency level."""

    title: str
    urgency: int


def process_task_str(text: str) -> Task:
    """Process the task."""
    text, urgency_str = text.split(",")
    try:
        urgency = int(urgency_str)
    except ValueError as e:
        msg = f"Incorrect value for urgency: {urgency_str!r} (expected an integer)."
        raise ValueError(msg) from e
    else:
        return Task(title=text, urgency=urgency)


def main() -> None:
    """Application entry point."""
    try:
        process_task_str("Do the laundry,#3")
    except ValueError as e:
        print(f"1: using {{e}}: Error processing task: {e}")
        print("2: using print(e): ", end="")
        print(e)
        print("3: using type(e): ", end="")
        print(type(e))
        print("4: using type(e).__name__: ", end="")
        print(type(e).__name__)


if __name__ == "__main__":
    main()
