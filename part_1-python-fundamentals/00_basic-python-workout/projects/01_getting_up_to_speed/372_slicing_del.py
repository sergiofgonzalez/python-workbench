"""Illustrate the use of the del statement with slicing."""


def main() -> None:
    """Application entry point."""
    x = ["a", 2, "c", 7, 9, 11]

    # Remove the second element
    del x[1]
    assert x == ["a", "c", 7, 9, 11]

    # Remove the first and second elements
    del x[0:2]
    assert x == [7, 9, 11]


if __name__ == "__main__":
    main()
