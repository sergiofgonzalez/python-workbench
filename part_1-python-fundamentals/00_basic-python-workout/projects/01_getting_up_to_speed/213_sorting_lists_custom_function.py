"""Illustrate how to sort a list with a custom function."""


def main() -> None:
    """Application entry point."""
    actors = ["Jennifer", "Idris", "Jason", "Florence", "Kenneth"]
    print("Original list:", actors)

    # using the built-in sorted() function to sort the list inline
    actors.sort()
    print("Sorted list (asc):", actors)

    # using the built-in sorted() function to sort the list inline
    actors.sort(reverse=True)
    print("Sorted list (desc):", actors)

    # now with a weird list
    print("-" * 80)
    lst = [3, 1, 2, "John", ["c", "a"], ["a", "b"]]
    print("Original weird list:", lst)

    # Trying to sort using the built-in sorted() function
    try:
        lst.sort()
    except TypeError as err:
        print("Error trying to sort the weird list:", err)

    # Sorting the weird list using a custom function
    lst.sort(key=lambda x: str(x))
    print("Sorted weird list:", lst)

    # There's a more succinct way to do the same using the built-in sorted() function
    lst2 = [3, 1, 2, "John", ["c", "a"], ["a", "b"]]
    lst2.sort(key=str)
    print("Sorted weird list:", lst2)

    # Another example with a list of dicts
    print("-" * 80)
    todos = [
        {"title": "Laundry", "desc": "Wash clothes", "urgency": 3},
        {"title": "Homework", "desc": "Physics + Math", "urgency": 5},
        {"title": "Museum", "desc": "Egyptian things", "urgency": 2},
    ]

    todos.sort(key=lambda x: x["urgency"])
    print("Sorted todos by urgency (asc):", todos)

    # Same thing can be done with a named function
    def get_urgency(todo: dict) -> int:
        """Get the urgency of a todo item."""
        return todo["urgency"]
    todos.sort(key=get_urgency, reverse=True)
    print("Sorted todos by urgency (desc):", todos)


if __name__ == "__main__":
    main()
