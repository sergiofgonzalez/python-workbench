"""Illustrate the syntax of format specifiers when using f-strings."""


def print_formatted_records(fmt: str) -> None:
    """Print records using the specified format."""
    task_ids = [1, 2, 3, 99999]
    task_names = ["Do homework", "Laundry", "Pay bills", "012345678901"]
    task_urgencies = [5, 3, 4, 999]

    print(f"{'task_id':{fmt}} {'task_name':{fmt}} {'task_urgency':{fmt}}")
    for task_id, task_name, task_urgency in zip(
        task_ids,
        task_names,
        task_urgencies,
        strict=True,
    ):
        print(f"{task_id:{fmt}} {task_name:{fmt}} {task_urgency:{fmt}}")


def main() -> None:
    """Application entry point."""
    task_ids = [1, 2, 3, 99999]
    task_names = ["Do homework", "Laundry", "Pay bills", "012345678901"]
    task_urgencies = [5, 3, 4, 999]

    print(f"{'task_id':^8} {'task_name':<12} {'task_urgency':^12}")
    for task_id, task_name, task_urgency in zip(
        task_ids,
        task_names,
        task_urgencies,
        strict=True,
    ):
        print(f"{task_id:^8} {task_name:<12} {task_urgency:^12}")

    # invoking a function to try out several format specifiers
    print()
    print_formatted_records("^20")

    print()
    print_formatted_records("<20")

    print()
    print_formatted_records(">20")

    print()
    print_formatted_records("*<20")

    print()
    print_formatted_records("*^20")


if __name__ == "__main__":
    main()
