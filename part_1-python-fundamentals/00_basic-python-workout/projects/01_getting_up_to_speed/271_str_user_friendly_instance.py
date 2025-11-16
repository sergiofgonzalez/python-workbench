"""Using __str__ for a user-friendly representation of a Task instance."""


class Task:
    """A simple task class with a status property."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the task with a title, description, and urgency level."""
        self.title = title
        self.description = description
        self.urgency = urgency

    def __str__(self) -> str:
        """User-friendly representation of a Task instance."""
        print(">>> __str__ called")
        return f"Task: {self.title} (Urgency: {self.urgency})"


def main() -> None:
    """Application entry point."""
    task = Task("Laundry", "Wash clothes", 3)
    print(task)

    user_friendly = str(task)
    print(f"User-friendly representation: {user_friendly}")


if __name__ == "__main__":
    main()
