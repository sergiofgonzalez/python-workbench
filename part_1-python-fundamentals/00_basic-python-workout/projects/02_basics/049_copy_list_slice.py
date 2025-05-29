"""Illustrate how to copy a list using the list slicing syntax."""


def main() -> None:
    """Application entry point."""
    l1 = ["one", 2, "a", False]

    # Copy the list using slicing
    l2 = l1[:]
    print(f"Original list: {l1}")
    print(f"Copied list: {l2}")
    assert l1 == l2
    assert l1 is not l2  # Ensure they are different objects
    assert id(l1) != id(l2)  # Ensure they have different memory addresses

    l2[0] = "changed"
    print(f"Original list: {l1}")
    print(f"Copied list: {l2}")
    assert l1 != l2



if __name__ == "__main__":
    main()
