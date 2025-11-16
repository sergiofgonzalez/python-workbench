"""Illustrate __new__ and __del__."""

import sys


class Task:
    """Represent a Task instance."""

    def __new__(cls, *args: object) -> "Task":
        """Task instance constructor."""
        instance = object.__new__(cls)
        print(f">> Task.__new__({args}) has been called")
        return instance

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Task instance initializer."""
        self.title = title
        self.description = description
        self.urgency = urgency
        print(f">> Task.__init__({title}, {description}, {urgency}) has been invoked")

    def __del__(self, *args: object) -> None:
        """Task instance destructor."""
        print(f"Task.__del__() has been invoked on {self}")

    def __repr__(self) -> str:
        """Developer-friendly representation of a Task instance."""
        attrs = ", ".join([f"{k} = {self.__dict__[k]!r}" for k in self.__dict__])
        return f"Task({attrs})"


def do_work() -> None:
    """Simulate working on a task."""
    task = Task("Bogus", "foobar", 55)
    print(f"Simulating work on {task}")
    print("done!")


def main() -> None:
    """Application entry point."""
    task = Task("Homework", "Physics + Math", 1)
    print(task)
    do_work()
    # you can force the invocation of the destructor using del
    # if you comment the next line, destructor will be called after done

    print(f"Ref count for task before del: {sys.getrefcount(task)} ")
    print(f"{"task" in locals()=}")
    del task
    print(f"{"task" in locals()=}")
    print("--done!")


if __name__ == "__main__":
    main()
