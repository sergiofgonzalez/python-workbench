"""Illustrates that self is just a convention, not a keyword."""


class Task:
    """A simple task class."""

    def __init__(this: "Task", title: str, description: str, urgency: int) -> None:  # type: ignore  # noqa: N805, PGH003
        """Initialize the task with a title, description, and urgency level."""
        this.title = title
        this.description = description
        this.urgency = urgency


def main() -> None:
    """Application entry point."""
    task = Task("Write report", "Write the annual report", 1)
    print(f"Task title: {task.title}")
    print(f"Task description: {task.description}")
    print(f"Task urgency: {task.urgency}")

if __name__ == "__main__":
    main()
