"""Illustrate how to add attributes on the fly in Python classes."""


class Task:
    """A simple task class."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the task with a title, description, and urgency level."""
        self.title = title
        self.description = description
        self.urgency = urgency

    def complete(self) -> None:
        """Mark the task as complete by adding a 'status' attribute."""
        self.status = "completed"

    def add_tag(self, tag: str) -> None:
        """Add a tag to the task by creating a 'tags' attribute if it doesn't exist."""
        if not hasattr(self, "tags"):
            self.tags = []
        self.tags.append(tag)

    def __repr__(self) -> str:
        """Developer-friendly representation of a Task instance."""
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"Task({attrs})"


class TaskV2:
    """A simple task class with predefined attributes."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the task with a title, description, and urgency level."""
        self.title = title
        self.description = description
        self.urgency = urgency
        self.status = "To Do"  # Predefine status attribute
        self.tags = []  # Predefine tags attribute

    def complete(self) -> None:
        """Mark the task as complete by adding a 'status' attribute."""
        self.status = "completed"

    def add_tag(self, tag: str) -> None:
        """Add a tag to the task."""
        self.tags.append(tag)

    def __repr__(self) -> str:
        """Developer-friendly representation of a TaskV2 instance."""
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"TaskV2({attrs})"


def main() -> None:
    """Application entry point."""
    task = Task("Homework", "Physics + Math", 3)
    print(f"{task=}")

    try:
        print(f"{task.status=}")
    except AttributeError as e:
        print(f"Caught an AttributeError as expected: {e}")

    task.complete()
    print(f"{task=}")
    print(f"{task.status=}")

    try:
        print(f"{task.tags=}")
    except AttributeError as e:
        print(f"Caught an AttributeError as expected: {e}")

    task.add_tag("school")
    task.add_tag("urgent")
    print(f"{task=}")
    print(f"{task.tags=}")
    print("===" * 10)

    task_v2 = TaskV2("Grocery Shopping", "Buy fruits and vegetables", 2)
    print(f"{task_v2=}")
    print(f"{task_v2.status=}")
    task_v2.complete()
    print(f"{task_v2=}")
    print(f"{task_v2.tags=}")
    task_v2.add_tag("personal")
    task_v2.add_tag("weekly")
    print(f"{task_v2=}")
    print(f"{task_v2.tags=}")


if __name__ == "__main__":
    main()
