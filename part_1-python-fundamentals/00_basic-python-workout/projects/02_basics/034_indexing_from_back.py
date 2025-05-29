"""Illustrate how to index from the back of a list."""


def main() -> None:
    """Application entry point."""
    l1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Getting the last element
    last_element = l1[-1]
    print(f"Last element: {last_element}")
    assert last_element == 10 # noqa: PLR2004

    # Getting the second to last element
    second_to_last_element = l1[-2]
    print(f"Second to last element: {second_to_last_element}")
    assert second_to_last_element == 9 # noqa: PLR2004

    # Getting the sublist containing the second to the one before last element
    sublist = l1[1:-1]
    print(f"Sublist from second to the one before last: {sublist}")
    assert sublist == [2, 3, 4, 5, 6, 7, 8, 9]

    # Getting the sublist containint the last, second to last, and third to last elements
    # in that order
    l2 = l1[-1:-4:-1]
    print(f"l2: {l2}")
    assert l2 == [10, 9, 8]




if __name__ == "__main__":
    main()
