"""Illustrate how to find an instance of a custom class in a list."""


class Task:
    """A task with a title and urgency level."""

    def __init__(self, title: str, urgency: int) -> None:
        """Initialize a Task instance."""
        self.title = title
        self.urgency = urgency

    def __repr__(self) -> str:
        """Return a string representation of the Task."""
        return f"Task(title={self.title!r}, urgency={self.urgency})"


tasks = [
    Task("Laundry", 3),
    Task("Museum", 4),
    Task("Homework", 5),
    Task("Ticket", 2),
]


class TaskV2:
    """A task with title and urgency that overrides __eq__ for in and index()."""

    def __init__(self, title: str, urgency: int) -> None:
        """Initialize a Task instance."""
        self.title = title
        self.urgency = urgency

    def __repr__(self) -> str:
        """Return a string representation of the Task."""
        return f"Task(title={self.title!r}, urgency={self.urgency})"

    def __eq__(self, other: object) -> bool:
        """Check for equality with another Task."""
        if not isinstance(other, TaskV2):
            return NotImplemented
        return self.title == other.title and self.urgency == other.urgency

    def __hash__(self) -> int:
        """Return a hash value for the TaskV2 instance."""
        return hash((self.title, self.urgency))


tasks2 = [
    TaskV2("Laundry", 3),
    TaskV2("Museum", 4),
    TaskV2("Homework", 5),
    TaskV2("Ticket", 2),
]


def main() -> None:
    """Application entry point."""
    # Locate task (if any) with urgency 5
    urgent_tasks = [task for task in tasks if task.urgency == 5]  # noqa: PLR2004
    assert len(urgent_tasks) == 1
    assert urgent_tasks[0].title == "Homework"
    print("urgent_tasks:", urgent_tasks)
    print("=== PASSED ===")

    # Finding a specific instance with 'in'
    homework = Task("Homework", 5)
    assert (homework in tasks) is False
    print(f"{id(homework)=:#x}")
    print(f"{id(tasks[2])=:#x}")

    # But you can use 'in' to locate the exact same instance
    assert tasks[2] in tasks
    print("=== PASSED ===")

    # Similarly, index() works with the exact same instance
    loc = tasks.index(tasks[2])
    assert loc == 2  # noqa: PLR2004
    print("=== PASSED ===")

    # But index() raises ValueError if the instance is different
    try:
        loc = tasks.index(homework)
    except ValueError as err:
        print(f"Error: {err}")
    print("=== PASSED ===")

    # You can tweak your custom class to make 'in' and 'index()' work based on
    # its values instead of their memory addresses by implementing __eq__
    # Now you can use 'in' to locate instance
    homework = TaskV2("Homework", 5)
    assert homework in tasks2
    print("=== PASSED ===")

    # And index()
    loc = tasks2.index(homework)
    assert loc == 2  # noqa: PLR2004
    print("=== PASSED ===")


if __name__ == "__main__":
    main()
