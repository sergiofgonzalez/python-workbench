"""A practical exercise in filtering an iterable."""


def main() -> None:
    """Application entry point."""
    tasks = [
        {"title": "Laundry", "desc": "Wash clothes", "urgency": 3},
        {"title": "Homework", "desc": "Physics + Math", "urgency": 5},
        {"title": "Museum", "desc": "Egyptian things", "urgency": 2},
    ]
    # Filtering out tasks with urgency level is less than or equal to 3
    urgent_tasks = {task["title"] for task in tasks if task["urgency"] > 3}  # noqa: PLR2004
    print(urgent_tasks)
    assert urgent_tasks == {"Homework"}
    print("=== PASSED(1) ===\n")

    # Same thing using filter() higher-order function
    urgent_tasks = {t["title"] for t in filter(lambda t: t["urgency"] > 3, tasks)}  # noqa: PLR2004
    print(urgent_tasks)
    assert urgent_tasks == {"Homework"}
    print("=== PASSED(2) ===\n")


if __name__ == "__main__":
    main()
