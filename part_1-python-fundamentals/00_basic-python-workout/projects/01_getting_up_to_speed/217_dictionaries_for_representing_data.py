"""Illustrate how to use dictionaries to represent basic domain model entities."""

data = """Laundry,Wash clothes,3
Homework,Physics + Math,5
Museum,Egyptian things,2
"""


def main() -> None:
    """Application entry point."""
    # Parse the data into a list of dicts
    tasks = []
    for line in data.strip().split("\n"):
        title, desc, urgency = line.split(",")
        task = {"title": title, "desc": desc, "urgency": int(urgency)}
        tasks.append(task)

    print("Tasks (dicts):", tasks)

    # Accessing fields by key
    for task in tasks:
        print(
            f"Title: {task['title']}, Desc: {task['desc']}, Urgency: {task['urgency']}",
        )

    # Dicts are mutable, so you can change their values
    tasks[0]["urgency"] = 4
    print("Updated first task:", tasks[0])

    # But you need to remember the keys, or you'll get a RuntimeError
    try:
        print(tasks[0]["urgency_level"])  # type: ignore  # noqa: PGH003
    except KeyError as err:
        print("Error trying to access a non-existing key in the dict:", err)

    # Creating views from tasks
    print("-" * 80)
    urgencies = {task["title"]: task["urgency"] for task in tasks}
    print("Urgencies view:", urgencies)

    # keys, values, and items are dynamic views on the dict
    print("-" * 80)
    print("Keys view:", urgencies.keys())
    print("Values view:", urgencies.values())
    print("Items view:", urgencies.items())

    urgencies["Go to the gym"] = 0
    print("Updated urgencies view:", urgencies)
    print("Keys view:", urgencies.keys())
    print("Values view:", urgencies.values())
    print("Items view:", urgencies.items())

    # Accesing a non-existing key raises a RuntimeError
    try:
        print(urgencies["Non-existing key"])  # type: ignore  # noqa: PGH003
    except KeyError as err:
        print("Error trying to access a non-existing key in the dict:", err)

    # This can be avoided using the get() method
    print("-" * 80)
    print("Accessing a non-existing key with get():", urgencies.get("Non-existing key"))
    print(
        "Accessing a non-existing key with get() and default:",
        urgencies.get("Non-existing key", 42),
    )

    # you can also use in but it is not very Pythonic
    print("-" * 80)
    print("Checking for a non-existing key with in:", "Non-existing key" in urgencies)
    print("Checking for an existing key with in:", "Laundry" in urgencies)


if __name__ == "__main__":
    main()
