"""Illustrate the use of `_` to accumulate items while unpacking."""


def main() -> None:
    """Application entry point."""
    task = (1001, "Laundry", "Wash clothes", "completed")
    task_id, *_, status = task
    print(f"Task ID: {task_id}")
    print(f"Status: {status}")
    assert task_id == 1001  # noqa: PLR2004
    assert status == "completed"

    # Also, you can explicitly use `_`  several times
    task = (1002, "Dishes", "Wash dishes", "in progress")
    task_id, _, _, status = task
    print(f"Task ID: {task_id}")
    print(f"Status: {status}")
    assert task_id == 1002  # noqa: PLR2004
    assert status == "in progress"

if __name__ == "__main__":
    main()
