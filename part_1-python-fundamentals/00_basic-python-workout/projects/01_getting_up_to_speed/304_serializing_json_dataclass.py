"""Illustrate how to serialize dataclasses into JSON."""

import json
from dataclasses import dataclass


@dataclass
class Task:
    """A simple task representation."""

    title: str
    description: str
    urgency: int


def main() -> None:
    """Application entry point."""
    task = Task("Buy groceries", "Milk, Bread, Eggs", 2)
    try:
        json.dumps(task)
    except Exception as e:  # noqa: BLE001
        print(f"Error serializing task: {e} (type={type(e).__name__})")

    # We can serialize it with a default function
    json_str = json.dumps(task, default=lambda o: o.__dict__)
    print(f"{json_str=}, type={type(json_str).__name__}")

    # This could have been done using __dict__ directly
    json_str2 = json.dumps(task.__dict__)
    print(f"{json_str2=}, type={type(json_str2).__name__}")


if __name__ == "__main__":
    main()
