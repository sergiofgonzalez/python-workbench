"""Illustrate the different techniques for sorting lists."""


def main() -> None:
    """Application entry point."""
    nums = [1, 4, 2, 6, 3, 5]

    # Sorting inline using sort()
    nums.sort()
    print(f"Sorted list using sort(): {nums}")
    assert nums == [1, 2, 3, 4, 5, 6]

    # Sorting inline a list with mixed types
    try:
        mixed = ["one", "two", "a", False]
        mixed.sort()
    except TypeError as e:
        print(f"Error sorting mixed types: {e}")

    # Getting a sorted copy of the list using sorted()
    nums = [1, 4, 2, 6, 3, 5]
    sorted_nums = sorted(nums)
    print(f"Original list: {nums}")
    print(f"Sorted copy using sorted(): {sorted_nums}")
    assert nums == [1, 4, 2, 6, 3, 5]
    assert sorted_nums == [1, 2, 3, 4, 5, 6]


if __name__ == "__main__":
    main()
