"""TODO: description of the program."""


class Task:
    """Represents a task with a title and urgency level."""

    def __init__(self, title: str) -> None:
        """Initialize the task with a title and urgency."""
        if not isinstance(title, str):
            msg = f"Expected str for title, got {type(title).__name__}"
            raise TypeError(msg)
        self.title = title


def main() -> None:
    """Application entry point."""
    try:
        Task(123) # pyright: ignore[reportArgumentType]
    except TypeError as e:
        print(f"Error creating task: {e}")


if __name__ == "__main__":
    main()
