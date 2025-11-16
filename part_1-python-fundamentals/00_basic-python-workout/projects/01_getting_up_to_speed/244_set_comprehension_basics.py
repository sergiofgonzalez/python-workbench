"""A practical exercise in set comprehension."""


def main() -> None:
    """Application entry point."""
    tasks = [
        {"title": "Laundry", "desc": "Wash clothes", "urgency": 3},
        {"title": "Homework", "desc": "Physics + Math", "urgency": 5},
        {"title": "Museum", "desc": "Egyptian things", "urgency": 2},
    ]

    task_titles = {task["title"] for task in tasks}
    assert task_titles == {"Laundry", "Homework", "Museum"}
    print("=== Passed! ===")


if __name__ == "__main__":
    main()
