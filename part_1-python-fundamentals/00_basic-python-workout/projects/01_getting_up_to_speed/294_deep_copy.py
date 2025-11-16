"""Illustrate deep copy in Python."""

import copy


class Task:
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
        """Developer-friendly representation of a Task instance."""
        attrs = ", ".join([f"{k} = {self.__dict__[k]!r}" for k in self.__dict__])
        return f"Task({attrs})"


def main() -> None:
    """Application entry point."""
    task = Task("Grocery", "Buy groceries", 2, ["shopping", "errands"])
    task_copy = copy.deepcopy(task)
    task.tags.append("weekly")

    # when using deep copy, the tags lists are different objects
    print("After modifying original task tags:")
    print(f"Original task tags: {task.tags}")
    print(f"Deep copied task tags: {task_copy.tags}")


if __name__ == "__main__":
    main()
