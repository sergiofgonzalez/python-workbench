"""Illustrate a few advanced slicing techniques."""


def main() -> None:
    """Application entry point."""
    x = [1, 2, 3, 4]

    # Extend the list with [4, 5, 6]
    x[len(x):] = [5, 6, 7]
    assert x == [1, 2, 3, 4, 5, 6, 7]

    # Prepend the list with [-1, 0]
    x[0:0] = [-1, 0]
    assert x == [-1, 0, 1, 2, 3, 4, 5, 6, 7]

    # Remove the elements from the second to the one before last
    x[1:-1] = []
    assert x == [-1, 7]

    # Reset the list
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Prepend the list with the third to last, second to last and last
    x[0:0] = x[-3:]
    assert x == [8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Remove the list from the third to last to the end
    x[-3:] = []
    assert x == [8, 9, 10, 1, 2, 3, 4, 5, 6, 7]


if __name__ == "__main__":
    main()
