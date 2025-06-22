"""Illustrate how to create a dict from two lists."""


def main() -> None:
    """Application entry point."""
    ids = [101, 102, 103]
    tasks = ["Laundry", "Homework", "Soccer"]

    # Using a dictionary comprehension to create a dict from two lists
    task_dict = dict(zip(ids, tasks, strict=True))
    print("Task dictionary:", task_dict)

    # Alternatively, using a for loop
    task_dict_loop = {}
    for i in range(len(ids)):
        task_dict_loop[ids[i]] = tasks[i]
    print("Task dictionary (using loop):", task_dict_loop)


if __name__ == "__main__":
    main()
