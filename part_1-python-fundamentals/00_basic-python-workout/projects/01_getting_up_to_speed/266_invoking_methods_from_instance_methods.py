"""Illustrate how to invoke methods from methods."""


class Task:
    """A simple task class."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the task with a title, description, and urgency level."""
        self.title = title
        self.description = description
        self.urgency = urgency
        self.status = "New"
        self.close_note = ""

    def complete(self, note: str = "") -> None:
        """Mark the task as complete by updating the 'status' attribute."""
        self.status = "Completed"
        self.close_note = note
        self.format_close_note()

    def format_close_note(self) -> None:
        """Return a formatted close note."""
        if self.close_note:
            self.close_note = self.close_note.title()
        else:
            self.close_note = "N/A."

    def __repr__(self) -> str:
        """Developer-friendly representation of a Task instance."""
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"Task({attrs})"


def main() -> None:
    """Application entry point."""
    task = Task("Laundry", "Wash and fold clothes", 3)
    print(task)
    print(f"Before completion: {task.status}")
    task.complete(note="clothes are clean and folded")
    print(f"After completion: {task.status}")
    print(task)
    print("=" * 20)

    # format close note is supposed to be called only internally, but Python
    # allows us to call it from outside as well
    another_task = Task("Grocery Shopping", "Buy fruits and veggies", 2)
    another_task.close_note = "bought fresh vegetables"
    another_task.format_close_note()
    print(another_task)


if __name__ == "__main__":
    main()
