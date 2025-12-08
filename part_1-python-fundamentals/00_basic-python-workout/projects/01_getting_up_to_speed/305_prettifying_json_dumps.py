"""Illustrate how to prettify JSON output using json.dumps extra arguments."""

import json
from dataclasses import dataclass


@dataclass
class Task:
    """A simple task representation."""

    title: str
    description: str
    urgency: int


@dataclass
class TaskV2:
    """A simple task representation with more fields."""

    title: str
    description: str
    urgency: int
    tags: list[str]


def main() -> None:
    """Application entry point."""
    task = Task("Buy groceries", "Milk, Bread, Eggs", 2)

    # Default JSON output
    json_str = json.dumps(task.__dict__)
    print(f"{json_str}")
    print("=" * 40)

    # Prettified JSON output
    json_str = json.dumps(
        task.__dict__,
        indent=2,
    )
    print(f"{json_str}")
    print("=" * 40)

    # Default JSON output for TaskV2
    task_v2 = TaskV2(
        "Prepare presentation",
        "Slides for the upcoming meeting",
        1,
        tags=["work", "urgent", "slides"],
    )
    json_str_v2 = json.dumps(task_v2.__dict__)
    print(f"{json_str_v2}")
    print("=" * 40)

    # Prettified JSON output for TaskV2
    json_str_v2 = json.dumps(
        task_v2.__dict__,
        indent=2,
    )
    print(f"{json_str_v2}")
    print("=" * 40)

    # Prettified JSON output with sorted keys for TaskV2
    json_str_v2 = json.dumps(
        task_v2.__dict__,
        indent=2,
        sort_keys=True,
    )
    print(f"{json_str_v2}")
    print("=" * 40)


if __name__ == "__main__":
    main()
