"""Flexible implementation of __repr__ using __class__/__name__."""

class Task:
    """A simple task class with a status property."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the task with a title, description, and urgency level."""
        self.title = title
        self.description = description
        self.urgency = urgency

    def __repr__(self) -> str:
        """Developer-friendly representation of a Task instance."""
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"


def main() -> None:
    """Application entry point."""
    task = Task("Laundry", "Wash clothes", 3)
    print(repr(task))



if __name__ == "__main__":
    main()
