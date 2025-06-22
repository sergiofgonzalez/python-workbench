"""Illustrate the use of zip_longest() vs. zip()."""

from itertools import zip_longest


def main() -> None:
    """Application entry point."""
    nums = range(3)
    letters = ["a", "b", "c", "d", "e"]

    # zip_longest() fills missing values with None by default
    zipped_longest = zip_longest(nums, letters)
    print(f"Zipped longest: {list(zipped_longest)}")

    # zip stops at the shortest iterable
    zipped = zip(nums, letters, strict=False)
    print(f"Zipped: {list(zipped)}")


if __name__ == "__main__":
    main()
