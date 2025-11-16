"""Illustrate how to use property setters."""


class Task:
    """A simple task class with a status property."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the task with a title, description, and urgency level."""
        self.title = title
        self.description = description
        self.urgency = urgency
        self._status = "New"  # Protected attribute

    @property
    def status(self) -> str:
        """Property to get the task status."""
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        """Property setter to update the task status."""
        if value not in {"New", "In Progress", "Suspended", "Completed"}:
            msg = "Status must be 'New', 'In Progress', 'Suspended', or 'Completed'."
            raise ValueError(msg)
        self._status = value

    def __repr__(self) -> str:
        """Developer-friendly representation of a Task instance."""
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"Task({attrs})"

    def __str__(self) -> str:
        """User-friendly representation of a Task instance."""
        return f"Task: {self.title} | Status: {self.status}"


def main() -> None:
    """Application entry point."""
    task = Task("Laundry", "Wash clothes", 3)
    print(f"{task!r}")
    print(task)

    task.status = "Suspended"
    print(task)

    try:
        task.status = "undefined"
    except ValueError as e:
        print(f"Oops: {e} ({type(e).__name__})")


if __name__ == "__main__":
    main()
