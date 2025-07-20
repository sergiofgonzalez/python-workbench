"""Illustrate the use case for '*' in func signatures."""


class Task:
    """A simple Task class that takes title, description, and urgency level."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize a task with title, description, and urgency level."""
        self.title = title
        self.description = description
        self.urgency = urgency


    def __repr__(self) -> str:
        """Return a string representation of the task using __dict__."""
        return f"Task({self.__dict__})"


def complete_task(task: Task, *, note: str = "") -> None:
    """Mark a task as complete and add a completion note."""
    task.status = "completed"  # type: ignore  # noqa: PGH003
    task.completion_note = note  # type: ignore  # noqa: PGH003


def main() -> None:
    """Application entry point."""
    lst = [4, 1, 3, 2]
    print(f"Original list: {lst}")

    lst.sort()  # Sorts the list in place
    print(f"Sorted list: {lst=}")

    lst.sort(reverse=True)  # Sorts the list in place in reverse order
    print(f"Reverse sorted list: {lst=}")

    # sort() signature is sort(*, key=None, reverse=False)
    # The '*' indicates that all parameters after it must be specified by keyword
    # This means you cannot pass key or reverse as positional arguments
    try:
        lst.sort(True)  # type: ignore  # noqa: FBT003, PGH003
    except TypeError as e:
        print(f"Error: {e}")

    # Playing with complete_task function
    task = Task(
        title="Finish project",
        description="Complete the Python project",
        urgency=1,
    )

    # You cannot pass 'note' as a positional argument due to the '*' in the signature
    try:
        complete_task(task, "Project completed successfully.") # type: ignore  # noqa: PGH003
        print(f"Task after completion: {task}")
    except TypeError as e:
        print(f"Error: {e}")

    # Correct usage with keyword argument
    complete_task(task, note="Project completed successfully.")
    print(f"Task after completion with note: {task}")

    # You can use the default value for note
    complete_task(task)
    print(f"Task after completion with default note: {task}")



if __name__ == "__main__":
    main()
