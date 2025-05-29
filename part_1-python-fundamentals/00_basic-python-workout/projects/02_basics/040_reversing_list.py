"""Illustrate how to reverse a list in Python using reverse()/reversed()."""


def main() -> None:
    """Application entry point."""
    nums = [1, 2, 3, 4, 5]

    # Reversing the list in place using reverse()
    nums.reverse()
    print(f"Reversed list using reverse(): {nums}")
    assert nums == [5, 4, 3, 2, 1]

    # Resetting the list
    nums = [1, 2, 3, 4, 5]

    # Reversing the list using reversed() and converting to a list
    reversed_nums = list(reversed(nums))
    print(f"Reversed list using reversed(): {reversed_nums}")
    assert reversed_nums == [5, 4, 3, 2, 1]
    assert nums == [1, 2, 3, 4, 5]  # Original list remains unchanged
    print("Original list remains unchanged after using reversed().")


if __name__ == "__main__":
    main()
