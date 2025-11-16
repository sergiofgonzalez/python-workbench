"""Using slice objects representing the slicing specs."""


def main() -> None:
    """Application entry point."""
    nums = list(range(1, 11))  # Create a list of numbers from 1 to 10
    print(nums)

    # Create a slice object to extract the even numbers
    even_slice = slice(1, None, 2)
    assert nums[even_slice] == [2, 4, 6, 8, 10]

    # We can apply the same slice object to other lists
    other_nums = list(range(101, 121))
    print(other_nums[even_slice])

if __name__ == "__main__":
    main()
