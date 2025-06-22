"""Illustrate how to use dict.fromkeys()."""


def main() -> None:
    """Application entry point."""
    keys = ["status", "urgency", "content"]

    # Using dict.fromkeys() to create a dictionary with default value None
    task = dict.fromkeys(keys)
    print("Task dictionary with None values:", task)

    # Using dict.fromkeys() to create a dictionary with a specific default value
    task_with_default = dict.fromkeys(keys, "N/A")
    print("Task dictionary with 'N/A' values:", task_with_default)


if __name__ == "__main__":
    main()
