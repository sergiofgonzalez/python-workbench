"""Illustate how to remove an item from a list by value."""


def main() -> None:
    """Application entry point."""
    nums = ["one", "two", "three", "two"]

    # Remove element "two" from the list
    nums.remove("two")
    print(f"List after removing 'two': {nums}")
    assert nums == ["one", "three", "two"]


if __name__ == "__main__":
    main()
