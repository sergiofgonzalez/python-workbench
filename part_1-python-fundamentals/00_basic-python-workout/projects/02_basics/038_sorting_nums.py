"""Illustrate the use of sorted() to sort numbers."""

from random import uniform


def main() -> None:
    """Application entry point."""
    nums = [uniform(0, 100) for _ in range(10)]  # noqa: S311
    print(f"Unsorted numbers: {nums}")

    # Sorting the list of numbers
    sorted_nums = sorted(nums)
    print(f"Sorted numbers: {sorted_nums}")

    # Verifying that the original list is unchanged
    assert nums != sorted_nums, "The original list should not be modified."
    print("Original list remains unchanged.")


if __name__ == "__main__":
    main()
