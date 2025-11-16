"""A practical example on property setters."""


class Task:
    """A simple task class with a status property."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the task with a title, description, and urgency level."""
        self.title = title
        self.description = description
        self._urgency = urgency

    @property
    def urgency(self) -> int:
        """Property getter for urgency."""
        return self._urgency

    @urgency.setter
    def urgency(self, value: int) -> None:
        """Property setter for urgency."""
        if not isinstance(value, int):
            msg = "Urgency must be an integer."
            raise TypeError(msg)
        if not (1 <= value <= 5):  # noqa: PLR2004
            msg = "Urgency must be between 1 and 5."
            raise ValueError(msg)
        self._urgency = value

    def __repr__(self) -> str:
        """Developer-friendly representation of a Task instance."""
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"Task({attrs})"


class TaskV2:
    """A simple task class with a status property, with updated urgency management."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the task with a title, description, and urgency level."""
        self.title = title
        self.description = description
        self.urgency = urgency

    @property
    def urgency(self) -> int:
        """Property getter for urgency."""
        return self._urgency

    @urgency.setter
    def urgency(self, value: int) -> None:
        """Property setter for urgency."""
        if not isinstance(value, int):
            msg = "Urgency must be an integer."
            raise TypeError(msg)
        if not (1 <= value <= 5):  # noqa: PLR2004
            msg = "Urgency must be between 1 and 5."
            raise ValueError(msg)
        self._urgency = value

    def __repr__(self) -> str:
        """Developer-friendly representation of a Task instance."""
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"TaskV2({attrs})"


def main() -> None:
    """Application entry point."""
    task = Task("Laundry", "Wash clothes", 3)
    print(f"Initial urgency: {task.urgency}")

    task.urgency = 5
    print(f"Updated urgency: {task.urgency}")

    try:
        task.urgency = "Highest"  # type: ignore  # noqa: PGH003
    except (ValueError, TypeError) as e:
        print(f"Oops: {e} ({type(e).__name__})")

    try:
        task.urgency = -1
    except (ValueError, TypeError) as e:
        print(f"Oops: {e} ({type(e).__name__})")

    try:
        task.urgency = -99
    except (ValueError, TypeError) as e:
        print(f"Oops: {e} ({type(e).__name__})")

    # However, we can initialize the task urgency to 99
    task = Task("Get some rest", "Relax over the weekend", 99)
    print(task)

    # This is solved in TaskV2
    try:
        _ = TaskV2("Get some rest", "Relax over the weekend", 99)
    except (ValueError, TypeError) as e:
        print(f"Oops: {e} ({type(e).__name__})")


if __name__ == "__main__":
    main()
