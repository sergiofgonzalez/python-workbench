"""Illustrate different ways to represent data in Python."""


def main() -> None:
    """Application entry point."""
    # A task with a title, description, and urgency level
    # represented as a list
    task1 = ["Laundry", "Wash clothes", 3]
    print("Task 1 (list):", task1)
    # You need unpacking to get the values
    title, desc, urgency = task1
    print(f"Title: {title}, Desc: {desc}, Urgency: {urgency}")
    # and you can change the values by index
    task1[2] = 4
    print("Updated Task 1 (list):", task1)

    # Same task represented as a tuple
    print("-" * 80)
    task2 = ("Homework", "Physics + Math", 5)
    print("Task 2 (tuple):", task2)
    # You need unpacking to get the values
    title, desc, urgency = task2
    print(f"Title: {title}, Desc: {desc}, Urgency: {urgency}")
    # but you cannot change the values as tuples are immutable
    try:
        task2[2] = 4  # type: ignore  # noqa: PGH003
    except TypeError as err:
        print("Error trying to update the tuple:", err)

    # Same task represented as a dict
    print("-" * 80)
    task3 = {"title": "Museum", "desc": "Egyptian things", "urgency": 2}
    print("Task 3 (dict):", task3)
    # You can get the values by key
    print(
        f"Title: {task3['title']}, Desc: {task3['desc']}, Urgency: {task3['urgency']}",
    )
    # and you can change the values by key
    task3["urgency"] = 1
    print("Updated Task 3 (dict):", task3)
    # but you need to remember the keys, or you'll get a RuntimeError
    try:
        print(task3["urgency_level"])  # type: ignore  # noqa: PGH003
    except KeyError as err:
        print("Error trying to access a non-existing key in the dict:", err)

    # Same task represented as a class
    print("-" * 80)
    class Task:
        """A task with a title, description, and urgency level."""

        def __init__(self, title: str, desc: str, urgency: int) -> None:
            self.title = title
            self.desc = desc
            self.urgency = urgency

        def __repr__(self) -> str:
            return f"Task(title={self.title}, desc={self.desc}, urgency={self.urgency})"
    task4 = Task("Grocery shopping", "Buy fruits and veggies", 4)
    print("Task 4 (class):", task4)
    # You can get the values by attribute
    print(f"Title: {task4.title}, Desc: {task4.desc}, Urgency: {task4.urgency}")
    # and you can change the values by attribute
    task4.urgency = 5
    print("Updated Task 4 (class):", task4)
    # but it's far more verbose

if __name__ == "__main__":
    main()
