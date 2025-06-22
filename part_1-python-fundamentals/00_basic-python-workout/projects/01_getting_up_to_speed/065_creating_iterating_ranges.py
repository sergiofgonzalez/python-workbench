"""Illustrate how to create and iterate over ranges."""


def main() -> None:
    """Application entry point."""
    nums = range(10)
    print(f"nums: {nums}")
    for num in nums:
        if num % 2 == 0:
            print(f"Even number: {num}")


if __name__ == "__main__":
    main()
