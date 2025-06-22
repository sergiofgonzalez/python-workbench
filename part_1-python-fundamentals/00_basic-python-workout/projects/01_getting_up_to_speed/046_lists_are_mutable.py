"""Illustrate that Python lists are mutable."""


def main() -> None:
    """Application entry point."""
    l1 = ["one", 2, "a", False]

    # Modify the second element of the list
    l1[1] = 14
    print(f"Modified list: {l1}")
    assert l1 == ["one", 14, "a", False]

    # Append a new element to the list
    l1.append("new")
    print(f"List after appending: {l1}")
    assert l1 == ["one", 14, "a", False, "new"]

    # Remove the first element from the list
    l1.remove("one")
    print(f"List after removing 'one': {l1}")
    assert l1 == [14, "a", False, "new"]

if __name__ == "__main__":
    main()
