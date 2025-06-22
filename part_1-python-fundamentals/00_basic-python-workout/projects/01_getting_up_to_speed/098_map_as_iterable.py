"""Illustrate how map creates a map iterator."""


def main() -> None:
    """Application entry point."""
    num_strings = ["1.23", "4.56", "7.89"]
    nums = map(float, num_strings)  # Create a map iterator
    print(nums)  # This will print a map object, not the numbers
    for num in nums:
        print(f"{num:.2f}")
    print("Done iterating over map object.")


if __name__ == "__main__":
    main()
