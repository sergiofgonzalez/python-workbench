"""Illustrates that mutable default values in function definitions are durable."""


def odd_numbers(lst: list[int], odds: list[int] = []) -> list[int]:  # noqa: B006
    """Append odd numbers from lst to odds and return odds.

    Args:
        lst (list[int]): List of integers to check.
        odds (list[int], optional): List to append odd numbers to. Defaults to [].

    Returns:
        list[int]: List of odd numbers.

    """
    for num in lst:
        if num % 2 != 0:
            odds.append(num)  # noqa: PERF401
    return odds


def main() -> None:
    """Application entry point."""
    lst = [1, 2, 3, 4, 5]
    print("First call to odd_numbers:", odd_numbers(lst))
    lst = [6, 7, 8, 9, 10]
    print("Second call to odd_numbers:", odd_numbers(lst))


if __name__ == "__main__":
    main()
