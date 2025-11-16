"""Illustrates how self is set by Python."""

from typing import Self


class MyClass:
    """A simple class to demonstrate self."""

    def __new__(cls, *args: object, **kwargs: object) -> Self:
        """Create a new instance of MyClass."""
        print("args:", args)
        print("kwargs:", kwargs)
        instance = super().__new__(cls)
        print(f"About to return a MyClass instance from __new__: {id(instance):#x}")
        return instance

    def __init__(self, value: int) -> None:
        """Initialize the instance with a value."""
        print(f"Initializing MyClass instance in __init__: {id(self):#x}")
        self.value = value


class Task:
    """A simple task class."""

    def __new__(cls, *args: object, **kwargs: object) -> Self:
        """Create a new instance of Task."""
        print("args:", args)
        print("kwargs:", kwargs)
        instance = super().__new__(cls)
        title, description, urgency = args
        # you could take some actions based on the args received, but you shouldn't
        # do the initialization here
        print(f"{title=}")
        print(f"{description=}")
        print(f"{urgency=}")
        print(f"About to return a Task instance from __new__: {id(instance):#x}")
        return instance

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the task with a title, description, and urgency level."""
        print(f"Initializing Task instance in __init__: {id(self):#x}")
        self.title = title
        self.description = description
        self.urgency = urgency


def main() -> None:
    """Application entry point."""
    obj = MyClass(42)  # type: ignore  # noqa: PGH003
    print(f"Object ID: {id(obj):#x}")
    print(f"Object value: {obj.value}")
    print("===" * 10)

    task = Task("Finish report", "Complete the annual report by end of day", 1)
    print(f"Task memory ID: {id(task):#x}")
    print(f"Task Title: {task.title}")
    print(f"Task Description: {task.description}")
    print(f"Task Urgency: {task.urgency}")
    print("===" * 10)

    # Explicit initialization of an instance without using the Task()
    other_task = Task.__new__(Task, "Homework", "Python + Go", 2)
    Task.__init__(other_task, "Homework", "Python + Go", 2)
    print(f"other_task memory address: {id(other_task):#x}")
    print(f"other_task.title: {other_task.title}")
    print(f"other_task.description: {other_task.description}")
    print(f"other_task.urgency: {other_task.urgency}")


if __name__ == "__main__":
    main()
