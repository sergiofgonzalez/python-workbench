"""Illustrates the basic of testing in Python."""


class Task:
    """A task with a title and urgency level."""

    def __init__(self, title: str, urgency: int) -> None:
        """Initialize a Task instance."""
        self.title = title
        self.urgency = urgency


def create_task_from_csv(csv_string: str) -> Task:
    """Create a Task instance from a CSV string."""
    title, urgency_str = csv_string.split(",")
    urgency = int(urgency_str)
    return Task(title, urgency)


def main() -> None:
    """Application entry point."""
    actual = create_task_from_csv("The title, 5")
    expected = Task("The title", 5)
    assert actual.__dict__ == expected.__dict__, "Assertion failed"


if __name__ == "__main__":
    main()
