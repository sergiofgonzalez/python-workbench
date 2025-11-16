"""Illustrating __repr__ for a developer-friendly representation of a Task instance."""


class Task:
    """A simple task class with a status property."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the task with a title, description, and urgency level."""
        self.title = title
        self.description = description
        self.urgency = urgency

    def __repr__(self) -> str:
        """Developer-friendly representation of a Task instance."""
        return (
            f"Task(title={self.title!r},"
            f" description={self.description!r}, "
            f"urgency={self.urgency!r})"
        )


class TaskV2:
    """A simple task class with a status property."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the task with a title, description, and urgency level."""
        self.title = title
        self.description = description
        self.urgency = urgency

    def __repr__(self) -> str:
        """Developer-friendly representation of a Task instance."""
        return (
            f"Task(title={self.title!r},"
            f" description={self.description!r}, "
            f"urgency={self.urgency!r})"
        )

    def __str__(self) -> str:
        """User-friendly representation of a Task instance."""
        return f"{self.title}: {self.description} (Urgency: {self.urgency})"


def main() -> None:
    """Application entry point."""
    task = Task("Laundry", "Wash clothes", 3)
    # print will invoke __repr__ when __str__ is not defined
    print(task)

    dev_friendly = repr(task)
    print(f"Developer-friendly representation: {dev_friendly}")
    print("===" * 10)
    task_v2 = TaskV2("Grocery Shopping", "Buy fruits and vegetables", 2)
    # print will invoke __str__ if defined
    print(task_v2)
    user_friendly = str(task_v2)
    print(f"User-friendly representation: {user_friendly}")
    dev_friendly_v2 = repr(task_v2)
    print(f"Developer-friendly representation: {dev_friendly_v2}")


if __name__ == "__main__":
    main()
