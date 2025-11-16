"""A practical exercise in dictionary comprehension."""


def main() -> None:
    """Application entry point."""
    tasks = [
        {"title": "Laundry", "desc": "Wash clothes", "urgency": 3},
        {"title": "Homework", "desc": "Physics + Math", "urgency": 5},
        {"title": "Museum", "desc": "Egyptian things", "urgency": 2},
    ]
    tasks_by_title = {task["title"]: task["desc"] for task in tasks}
    print(tasks_by_title)


if __name__ == "__main__":
    main()
