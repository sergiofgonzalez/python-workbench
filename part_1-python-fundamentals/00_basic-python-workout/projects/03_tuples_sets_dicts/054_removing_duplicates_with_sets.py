"""Illustrate how to remove duplicates from a list using sets."""

from random import randint


def count_draws_until_all_digits_0_9_found() -> int:
    """Return how many random numbers were generated until we get 0-9 set."""
    done = False
    numbers = set()
    i = 0
    while not done:
        num = randint(0, 10)  # noqa: S311
        i += 1
        numbers.add(num)
        if len(numbers) == 10:  # noqa: PLR2004
            done = True
    return i


def main() -> None:
    """Application entry point."""
    nums = [randint(0, 10) for _ in range(100)]  # noqa: S311
    unique_nums = list(set(nums))
    print("Original list:", nums)
    print("List with duplicates removed:", unique_nums)

    print("Number of draws until we get all digits from 0 to 9:")
    iterations = [count_draws_until_all_digits_0_9_found() for _ in range(1000)]
    print("Average iterations:", sum(iterations) / len(iterations))
    print("Minimum iterations:", min(iterations))
    print("Maximum iterations:", max(iterations))


if __name__ == "__main__":
    main()
