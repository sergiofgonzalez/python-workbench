"""Illustrate nested loops and list comprehension."""


def main() -> None:
    """Application entry point."""
    tasks = [
        {"title": "Laundry", "desc": "Wash clothes", "urgency": 3},
        {"title": "Homework", "desc": "Physics + Math", "urgency": 5},
        {"title": "Museum", "desc": "Egyptian things", "urgency": 2},
    ]
    # Flattening the list using nested loops
    flattened_tasks = []
    for task in tasks:
        for value in task.values():
            flattened_tasks.append(value)  # noqa: PERF402
    assert flattened_tasks == [
        "Laundry",
        "Wash clothes",
        3,
        "Homework",
        "Physics + Math",
        5,
        "Museum",
        "Egyptian things",
        2,
    ]

    # Same thing using list comprehension
    flattened_tasks = [value for task in tasks for value in task.values()]
    assert flattened_tasks == [
        "Laundry",
        "Wash clothes",
        3,
        "Homework",
        "Physics + Math",
        5,
        "Museum",
        "Egyptian things",
        2,
    ]


if __name__ == "__main__":
    main()
