"""How to deserialize an array of JSON objects into dataclass instances."""

import json
from dataclasses import dataclass


@dataclass
class Task:
    """Represents a task with a title, description, and urgency level."""

    def __init__(self, title: str, desc: str, urgency: int) -> None:
        """Initialize a Task instance."""
        self.title = title
        self.desc = desc
        self.urgency = urgency

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a Task instance from a dictionary."""
        return cls(
            title=data["title"],
            desc=data["desc"],
            urgency=data["urgency"],
        )

    def __repr__(self) -> str:
        """Return a string representation of the Task."""
        return f"Task(title={self.title!r}, desc={self.desc!r}, urgency={self.urgency})"


def main() -> None:
    """Application entry point."""
    json_string = """
    [
        {
            "title": "Laundry",
            "desc": "Wash clothes",
            "urgency": 3
        },
        {
            "title": "Homework",
            "desc": "Physics + Math",
            "urgency": 5
        }
    ]
    """
    # Plain deserialization does not produce the expected results
    python_list_of_objs = json.loads(json_string)
    print(python_list_of_objs)

    # We can iterate over the list of deserialized objects: they are dicts
    for item in json.loads(json_string):
        print(f"Item: {item}, Type: {type(item).__name__}")

    # We can bank on those dicts and  create Task instances manually
    tasks = []
    for item in json.loads(json_string):
        task = Task(
            title=item["title"],
            desc=item["desc"],
            urgency=item["urgency"],
        )
        tasks.append(task)

    print(tasks)
    print("=" * 40)

    # We can do it more concisely using a list comprehension
    tasks_comp = [
        Task(
            title=item["title"],
            desc=item["desc"],
            urgency=item["urgency"],
        )
        for item in json.loads(json_string)
    ]
    print(tasks_comp)
    print("=" * 40)

    # And even clearer using argument unpacking
    tasks_unpack = [Task(**item) for item in json.loads(json_string)]
    print(tasks_unpack)
    print("=" * 40)

    # It's also a common pattern to define a factory method on the class
    tasks_factory = [Task.from_dict(item) for item in json.loads(json_string)]
    print(tasks_factory)


if __name__ == "__main__":
    main()
