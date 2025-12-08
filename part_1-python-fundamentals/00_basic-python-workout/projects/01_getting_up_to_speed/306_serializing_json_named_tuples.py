"""Illustrate how to serialize NamedTuples to JSON."""

import json
from typing import NamedTuple


class Task(NamedTuple):
    """A simple task with a title, description, and urgency level."""

    title: str
    description: str
    urgency: int


def main() -> None:
    """Application entry point."""
    task = Task("Homework", "Physics and math", 5)

    # Default JSON output is not probably what you want
    json_str = json.dumps(task)
    print(f"{json_str=}")

    # We can serialize it with a default function, but __dict__ won't give you
    # the expected results either
    json_str = json.dumps(task, default=lambda t: t.__dict__)
    print(f"{json_str=}")

    # The best way is to convert it to a dictionary using _asdict()
    json_str = json.dumps(task._asdict())
    print(f"{json_str=}")

    # Using a custom serialization function won't work, because
    # the encoder function is not called for NamedTuples by default
    def serialize_namedtuple(obj: Task) -> dict:
        if isinstance(obj, Task):  # type: ignore  # noqa: PGH003
            return {
                "title": obj.title,
                "description": obj.description,
                "urgency": obj.urgency,
            }
        msg = f"Type {type(obj)} not serializable"
        raise TypeError(msg)

    json_str = json.dumps(task, default=serialize_namedtuple)
    print(f"{json_str=}")


if __name__ == "__main__":
    main()
