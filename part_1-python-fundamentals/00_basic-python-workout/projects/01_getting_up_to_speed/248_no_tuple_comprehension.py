"""Validate that there's no tuple comprehension (generators are created instead)."""


def main() -> None:
    """Application entry point."""
    # Looks like a tuple comprehension,  but that syntax cretes a generator
    task1 = ["Laundry", "Wash clothes", 3]
    task_tuple = (item for item in task1)
    print(f"{task_tuple} type={type(task_tuple).__name__}")

    # If you want to create a tuple, use tuple() instead
    my_tuple = tuple(task1)
    assert my_tuple == ("Laundry", "Wash clothes", 3)

    # If you want to create a tuple dynamicall, use a list comprehension
    # and then transform into a tuple
    # e.g. tuple with task1 items in uppercase
    tasks_upper = tuple([str(item).upper() for item in task1])
    print(tasks_upper)


if __name__ == "__main__":
    main()
