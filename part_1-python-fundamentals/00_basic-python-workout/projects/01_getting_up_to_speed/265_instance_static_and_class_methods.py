"""Illustrate how create instance, static, and class methods."""

from datetime import UTC, datetime


class Task:
    """A simple task class."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the task with a title, description, and urgency level."""
        self.title = title
        self.description = description
        self.urgency = urgency
        self.status = "New"

    def complete(self) -> None:
        """Mark the task as complete by updating the 'status' attribute."""
        self.status = "Completed"

    @classmethod
    def task_from_dict(cls, input_dict: dict) -> "Task":
        """Create a Task instance from a dictionary."""
        return cls(
            title=input_dict.get("title", "No Title"),
            description=input_dict.get("description", "No Description"),
            urgency=input_dict.get("urgency", 1),
        )

    @staticmethod
    def get_current_ts() -> str:
        """Return the current UTC timestamp in the format Oct 25, 2025 09:17."""
        return datetime.now(tz=UTC).strftime("%b %d %Y, %H:%M")

    def __repr__(self) -> str:
        """Developer-friendly representation of a Task instance."""
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"Task({attrs})"


def main() -> None:
    """Application entry point."""
    task = Task("Homework", "Physics + Math", 3)
    print(f"Before completion: {task.status}")
    task.complete()
    print(f"After completion: {task.status}")
    print("=" * 20)

    task_data = {
        "title": "Grocery Shopping",
        "description": "Buy fruits and vegetables",
        "urgency": 2,
    }
    new_task = Task.task_from_dict(task_data)
    print(
        "New Task from dict: ",
        f"{new_task.title}, {new_task.description}, {new_task.urgency}",
    )
    print("new task:", new_task)
    print("=" * 20)

    current_ts = Task.get_current_ts()
    print(f"Current Timestamp: {current_ts}")


if __name__ == "__main__":
    main()
