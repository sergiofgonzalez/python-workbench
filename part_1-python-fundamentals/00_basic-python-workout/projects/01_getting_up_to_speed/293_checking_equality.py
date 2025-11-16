"""Illustrate how to check equality in Python with is and ==."""


class Task:
    """Represents a task."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize a Task instance."""
        self.title = title
        self.description = description
        self.urgency = urgency

    def __eq__(self, other: object) -> bool:
        """Check equality between two Task instances."""
        if not isinstance(other, Task):
            return NotImplemented
        return (
            self.title == other.title
            and self.description == other.description
            and self.urgency == other.urgency
        )

    def __hash__(self) -> int:
        """Return a hash value for the Task instance."""
        return hash((self.title, self.description, self.urgency))

    def __repr__(self) -> str:
        """Developer-friendly representation of a Task instance."""
        attrs = ", ".join([f"{k} = {self.__dict__[k]!r}" for k in self.__dict__])
        return f"Task({attrs})"


def main() -> None:
    """Application entry point."""
    task1 = Task("Homework", "Physics + Math", 1)
    task2 = Task("Homework", "Physics + Math", 1)
    task3 = task1

    # if __eq__ is not defined, the default behavior is to check identity
    # i.e., whether both references point to the same object in memory
    # if defined, __eq__ should check for value equality
    print(f"task1 is task2: {task1 is task2}")  # identity check
    print(f"task1 == task2: {task1 == task2}")  # equality check

    print(f"task1 is task3: {task1 is task3}")  # identity check
    print(f"task1 == task3: {task1 == task3}")  # equality check


if __name__ == "__main__":
    main()
