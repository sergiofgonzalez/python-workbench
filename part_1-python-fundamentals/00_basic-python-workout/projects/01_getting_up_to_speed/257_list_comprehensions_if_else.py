"""Illustrate the use of if-else in list comprehensions."""


def main() -> None:
    """Application entry point."""
    # regular list comprehension for getting even numbers
    even_nums = [num for num in range(1, 11) if num % 2 == 0]
    print(f"even numbers: {even_nums}")

    # if-else syntax is a bit different
    nums = [0 if num == 5 else num for num in range(10)]  # noqa: PLR2004
    print(f"zeroized 5: {nums}")


if __name__ == "__main__":
    main()
