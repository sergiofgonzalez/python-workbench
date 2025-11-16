"""Illustrate the Python conventions for protected and private methods."""


class Task:
    """A simple task class."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the task with a title, description, and urgency level."""
        self.title = title
        self.description = description
        self.urgency = urgency
        self._status = "New"  # Protected attribute
        self._close_note = ""  # Protected attribute

    def complete(self, note: str = "") -> None:
        """Mark the task as complete by updating the '_status' attribute."""
        self._status = "Done"
        self._close_note = note
        self.__format_close_note()

    def __format_close_note(self) -> None:
        """Private method to format the close note."""
        if self._close_note:
            self._close_note = self._close_note.title()
        else:
            self._close_note = "N/A"

    def __repr__(self) -> str:
        """Developer-friendly representation of a Task instance."""
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"Task({attrs})"


def main() -> None:
    """Application entry point."""
    task = Task("Laundry", "Wash and fold clothes", 3)
    print(task)

    task.complete(note="clothes are clean and folded")
    print(task)

    # Accessing protected attribute (not recommended, but possible):
    # requires linting exception
    print(f"Task status (accessing protected): {task._status}")  # noqa: SLF001
    print(f"Task close note (accessing protected): {task._close_note}")  # noqa: SLF001

    # Trying to access private method will raise an AttributeError
    try:
        task.__format_close_note()  # noqa: SLF001
    except AttributeError as e:
        print(f"Error: {e}")

    print(f"{task.__dict__=}")
    print(f"{task.__dir__()=}")



if __name__ == "__main__":
    main()
