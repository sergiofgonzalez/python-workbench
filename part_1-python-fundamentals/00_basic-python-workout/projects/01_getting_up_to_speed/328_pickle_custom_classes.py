"""Illustrates how to pickle and unpickle custom classes."""

import pickle
from pathlib import Path


class Task:
    """Represents a task with an id, a title, and an urgency value."""

    def __init__(self, task_id: str, title: str, urgency: int) -> None:
        """Initialize a Task instance."""
        self.task_id = task_id
        self.title = title
        self.urgency = urgency

    def __repr__(self) -> str:
        """Developer-friendly representation of a Task instance."""
        attrs = ",".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"


def main() -> None:
    """Application entry point."""
    task = Task("1001", "Python", 1)

    file_path = Path("data/out_data/tmp/task.pkl")
    with file_path.open(mode="wb") as file:
        pickle.dump(task, file)

    # Now we unpickle
    with file_path.open(mode="rb") as file:
        unpickled_task = pickle.load(file)  # noqa: S301

    print(unpickled_task)

    # The class must be known at the time of unpickling
    del globals()["Task"]  # remove the class from the scope

    try:
        with file_path.open(mode="rb") as file:
            _ = pickle.load(file)  # noqa: S301

    except Exception as e:  # noqa: BLE001
        print(f"Error unpickling: {e} (type={type(e).__name__})")


if __name__ == "__main__":
    main()
