"""Safely removing an item from a list."""


def safe_remove(item: int, lst: list[object]) -> None:
    """Remove an item from a list if it exists.

    Args:
        item: The item to remove.
        lst: The list from which to remove the item.

    """
    if item in lst:
        lst.remove(item)


def safe_remove_v2(item: int, lst: list[object]) -> None:
    """Remove an item from a list if if the item occurs in the list more than once.

    Args:
        item: The item to remove.
        lst: The list from which to remove the item.

    """
    if lst.count(item) > 1:
        lst.remove(item)


def main() -> None:
    """Application entry point."""
    numbers: list[object] = [1, 2, 3, 4, 5]
    print(f"Original list: {numbers}")

    safe_remove(3, numbers)
    print(f"After removing 3: {numbers}")

    safe_remove(6, numbers)  # 6 is not in the list
    print(f"After trying to remove 6: {numbers}")
    print("=" * 40)

    numbers = [1, 2, 2, 3, 4, 5]
    print(f"Original list: {numbers}")
    safe_remove_v2(2, numbers)
    print(f"After removing one occurrence of 2: {numbers}")
    safe_remove_v2(3, numbers)  # 3 occurs only once
    print(f"After trying to remove 3: {numbers}")


if __name__ == "__main__":
    main()
