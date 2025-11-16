"""Illustrate how to create a read-only property using the property decorator."""


class Task:
    """A simple task class with a read-only status property."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the task with a title, description, and urgency level."""
        self.title = title
        self.description = description
        self.urgency = urgency
        self._status = "New"  # Protected attribute

    @property
    def status(self) -> str:
        """Read-only property to get the task status."""
        return self._status

    def complete(self) -> None:
        """Mark the task as complete by updating the '_status' attribute."""
        self._status = "Done"

    def __repr__(self) -> str:
        """Developer-friendly representation of a Task instance."""
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"Task({attrs})"

    def __str__(self) -> str:
        """User-friendly string representation of the Task."""
        return f"Task: {self.title} | Status: {self.status}"


def main() -> None:
    """Application entry point."""
    task = Task("Laundry", "Wash and fold clothes", 3)
    print(f"{task!r}")
    print(task)
    print(f"Initial task status: {task.status}")
    task.complete()
    print(f"{task!r}")
    print(task)
    print(f"Updated task status: {task.status}")

    # trying to hack the read-only property will raise an AttributeError
    try:
        task.status = "In Progress" # type: ignore  # noqa: PGH003
    except AttributeError as e:
        print(f"Error: {e}")

    # direct access to the protected attribute
    task._status = "In Progress"    # noqa: SLF001
    print(f"Directly modified task status: {task.status}")


if __name__ == "__main__":
    main()
