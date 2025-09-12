"""Illustrates how to catch multiple exceptions in a single except block."""


def process_task(text: str) -> None:
    """Process the task."""
    text, urgency_str = text.split(",")
    urgency = int(urgency_str)
    pending_task = ""
    # this will fail
    pending_task.title = text  # pyright: ignore[reportAttributeAccessIssue]
    pending_task.urgency = urgency  # pyright: ignore[reportAttributeAccessIssue]


def main() -> None:
    """Application entry point."""
    # This should catch a ValueError
    try:
        process_task("Complete the report,high")
    # The except block catches both ValueError and AttributeError in a single
    # except block
    except (ValueError, AttributeError) as e:
        print(f"An error occurred: {e} (type={type(e).__name__})")

    # This should catch an AttributeError
    try:
        process_task("Complete the report,1")
    # The except block catches both ValueError and AttributeError in a single
    # except block
    except (ValueError, AttributeError) as e:
        print(f"An error occurred: {e} (type={type(e).__name__})")


if __name__ == "__main__":
    main()
