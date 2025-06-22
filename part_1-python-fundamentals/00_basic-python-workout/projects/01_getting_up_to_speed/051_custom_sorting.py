"""Illustrate how to do custom sorting in Python."""


def main() -> None:
    """Application entry point."""
    workmates = ["Eloy", "carlos", "antonio", "ascen", "gloria"]
    print(f"Original list: {workmates}")

    # Get a sorted list with the default sort order
    sorted_workmates = sorted(workmates)
    print(f"Sorted list (default order): {sorted_workmates}")
    assert sorted_workmates == ["Eloy", "antonio", "ascen", "carlos", "gloria"]

    # Get a sorted list with a custom sort order (case-insensitive)
    sorted_workmates_case_insensitive = sorted(workmates, key=str.lower)
    print(f"Sorted list (case-insensitive): {sorted_workmates_case_insensitive}")
    assert sorted_workmates_case_insensitive == [
        "antonio",
        "ascen",
        "carlos",
        "Eloy",
        "gloria",
    ]


if __name__ == "__main__":
    main()
