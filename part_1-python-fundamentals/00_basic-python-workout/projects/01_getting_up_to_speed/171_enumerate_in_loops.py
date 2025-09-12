"""Illustrate how to emulate imperative loops with enumerate."""


def main() -> None:
    """Application entry point."""
    nums = range(50, 55)
    for i, num in enumerate(nums):
        print(f"{i}: {num}")


if __name__ == "__main__":
    main()
