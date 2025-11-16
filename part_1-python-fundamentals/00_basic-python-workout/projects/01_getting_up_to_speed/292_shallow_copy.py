"""Illustrates shallow copying in Python."""

from copy import copy


class Task:
    """Represents a task."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize a Task instance."""
        self.title = title
        self.description = description
        self.urgency = urgency

    def __repr__(self) -> str:
        """Developer-friendly representation of a Task instance."""
        attrs = ", ".join([f"{k} = {self.__dict__[k]!r}" for k in self.__dict__])
        return f"Task({attrs})"


class TaskV2:
    """Represents a task with a list of tags."""

    def __init__(
        self,
        title: str,
        description: str,
        urgency: int,
        tags: list[str],
    ) -> None:
        """Initialize a TaskV2 instance."""
        self.title = title
        self.description = description
        self.urgency = urgency
        self.tags = tags

    def __repr__(self) -> str:
        """Developer-friendly representation of a TaskV2 instance."""
        attrs = ", ".join([f"{k} = {self.__dict__[k]!r}" for k in self.__dict__])
        return f"TaskV2({attrs})"


def main() -> None:
    """Application entry point."""
    task = Task("Homework", "Physics + Math", 1)
    print(f"Original task: {task}")

    shallow_copied_task = copy(task)
    print(f"Shallow copied task: {shallow_copied_task}")

    task.title = "Modified Homework"
    print("After modifying original task title:")
    print(f"Original task: {task}")
    print(f"Shallow copied task: {shallow_copied_task}")
    print("===" * 20)

    # Now illustrate shallow copy with mutable attributes
    task_v2 = TaskV2("Grocery", "Buy groceries", 2, ["shopping", "errands"])
    shallow_copied_task_v2 = copy(task_v2)
    task_v2.tags.append("weekly")
    # In this case both tags are aliased to the same list object
    print(f"Original TaskV2 tags: {task_v2.tags}")
    print(f"Shallow copied TaskV2 tags: {shallow_copied_task_v2.tags}")
    print("===" * 20)


if __name__ == "__main__":
    main()
