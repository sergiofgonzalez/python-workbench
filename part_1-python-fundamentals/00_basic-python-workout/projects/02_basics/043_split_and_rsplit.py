"""Illustrate the use of split() and rsplit() methods."""


def main() -> None:
    """Application entry point."""
    str = """This is line 1
This is line 2
This is line 3
This is line 4
This is line 5"""

    # Using split() to split the string into lines
    lines = str.split("\n")
    print(f"Using split(): {lines}")
    assert lines == [
        "This is line 1",
        "This is line 2",
        "This is line 3",
        "This is line 4",
        "This is line 5",
    ]

    # Using split() to get the first three lines and the rest as a single string
    lines = str.split("\n", 3)
    print(f"Using split() with maxsplit=3: {lines}")
    assert lines == [
        "This is line 1",
        "This is line 2",
        "This is line 3",
        "This is line 4\nThis is line 5",
    ]

    # Using rsplit() to split the string into lines
    lines = str.rsplit("\n")
    print(f"Using rsplit(): {lines}")
    assert lines == [
        "This is line 1",
        "This is line 2",
        "This is line 3",
        "This is line 4",
        "This is line 5",
    ]

    # Using rsplit() to get the last three lines and the rest as a single string
    lines = str.rsplit("\n", 3)
    print(f"Using rsplit() with maxsplit=3: {lines}")
    assert lines == [
        "This is line 1\nThis is line 2",
        "This is line 3",
        "This is line 4",
        "This is line 5",
    ]


if __name__ == "__main__":
    main()
