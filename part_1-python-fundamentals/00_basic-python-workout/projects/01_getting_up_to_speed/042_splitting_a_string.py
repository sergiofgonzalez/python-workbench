"""Illustate how to use split() to create a list of lists from a string."""


def main() -> None:
    """Application entry point."""
    s = """1001,Homework,5
1002,Laundry,3
1003,Grocery,4"""

    # Splitting the string into lines
    lines = s.splitlines()
    print(f"Lines: {lines}")
    assert lines == ["1001,Homework,5", "1002,Laundry,3", "1003,Grocery,4"]
    # Splitting each line into a list of values
    list_of_lists = [line.split(",") for line in lines]
    print(f"List of lists: {list_of_lists}")
    assert list_of_lists == [
        ["1001", "Homework", "5"],
        ["1002", "Laundry", "3"],
        ["1003", "Grocery", "4"],
    ]


if __name__ == "__main__":
    main()
