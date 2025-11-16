"""Illustrate how to use __dict__ in classes to get the instance attributes."""


class Task:
    """A simple task class."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the task with a title, description, and urgency level."""
        self.title = title
        self.description = description
        self.urgency = urgency

    def __repr__(self) -> str:
        """Developer-friendly representation of a Task instance."""
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"Task({attrs})"


def main() -> None:
    """Application entry point."""
    task = Task("Homework", "Physics + Math", 3)
    print(f"{task.__dict__=}")

    # changing the attribute values through `__dict__`
    task.__dict__["title"] = "Math Homework"
    task.__dict__["description"] = "Complete the math exercises"
    task.__dict__["urgency"] = 2
    print(f"{task.title=}")
    print(f"{task.description=}")
    print(f"{task.urgency=}")
    print("=" * 20)

    # defining more attributes on the fly
    task.__dict__["tags"] = ["school", "boring stuff"]
    print(f"{task.title=}")
    print(f"{task.description=}")
    print(f"{task.urgency=}")
    print(f"{task.tags=}")  # type: ignore  # noqa: PGH003

    # using repr
    print("=" * 20)
    print(task)


if __name__ == "__main__":
    main()
