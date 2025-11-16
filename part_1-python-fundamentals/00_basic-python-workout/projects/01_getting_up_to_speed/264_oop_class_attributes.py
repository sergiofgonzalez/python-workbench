"""Ill."""


class Task:
    """A simple task class."""

    user = "logged in user"

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the task with a title, description, and urgency level."""
        self.title = title
        self.description = description
        self.urgency = urgency

    def __repr__(self) -> str:
        """Developer-friendly representation of a Task instance."""
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"Task({self.user!r}, {attrs})"


def main() -> None:
    """Application entry point."""
    task = Task("Homework", "Physics + Math", 3)
    print(f"{task=}")


if __name__ == "__main__":
    main()
