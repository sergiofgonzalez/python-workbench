"""Illustrates setUp method  of unittest testing framework."""

import unittest


class Task:
    """Represents a task with a title and urgency level."""

    def __init__(self, title: str, urgency: int) -> None:
        """Initialize a Task instance."""
        self.title = title
        self.urgency = urgency


def create_task_from_csv_string(csv_string: str) -> Task:
    """Return an initialized task instance from a CSV string."""
    title, urgency = csv_string.split(",")
    return Task(title, int(urgency))


def create_task_from_dict(task_dict: dict[str, str | int]) -> Task:
    """Return an initialized task instance from a dictionary."""
    title: str = str(task_dict["title"])
    urgency: int = int(task_dict["urgency"])
    return Task(title, urgency)


class TaskTestCase(unittest.TestCase):
    """Test Case for the Task class."""

    def setUp(self) -> None:
        """Prepare the execution for each of the tests."""
        self.title = "the title"
        self.urgency = 543
        self.expected = Task(self.title, self.urgency)

    def test_create_task_from_csv_string(self) -> None:
        """Test create_task_from_csv_string instance method."""
        actual = create_task_from_csv_string(f"{self.title},{self.urgency}")
        self.assertEqual(actual.__dict__, self.expected.__dict__)  # noqa: PT009

    def test_create_task_from_dict(self) -> None:
        """Test create_task_from_dict instance method."""
        actual = create_task_from_dict({"title": self.title, "urgency": self.urgency})
        self.assertEqual(actual.__dict__, self.expected.__dict__)  # noqa: PT009



if __name__ == "__main__":
    unittest.main()
