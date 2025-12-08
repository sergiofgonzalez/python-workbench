"""Serializing custom classes to JSON."""

import json


class Task:
    """A simple task representation."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the Task instance."""
        self.title = title
        self.description = description
        self.urgency = urgency


def main() -> None:
    """Application entry point."""
    task = Task("Finish report", "Complete the annual report", 3)

    # Default JSON output will raise an error
    try:
        json_str = json.dumps(task)
    except TypeError as e:
        print(f"Error serializing task: {e}")

    # We can serialize it with a default function
    json_str = json.dumps(task, default=lambda o: o.__dict__)
    print(f"{json_str=}")

    # This could have been done using __dict__ directly
    json_str2 = json.dumps(task.__dict__)
    print(f"{json_str2=}")

    # Using a custom serialization function
    def serialize_task(obj: Task) -> dict:
        if isinstance(obj, Task):  # type: ignore  # noqa: PGH003
            return {
                "title": obj.title,
                "description": obj.description,
                "urgency": obj.urgency,
            }
        msg = f"Type {type(obj)} not serializable"
        raise TypeError(msg)

    json_str3 = json.dumps(task, default=serialize_task)
    print(f"{json_str3=}")


if __name__ == "__main__":
    main()
