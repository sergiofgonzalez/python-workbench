"""Creating and accessing sets."""

def main() -> None:
    """Application entry point."""
    nums = {0, 1, 2, 3, 4, 5}
    print("nums:", nums)
    print("Length of nums:", len(nums))
    try:
        print("Third element of nums:", nums[2]) # type: ignore
    except TypeError as e:
        print("Error:", e)

    # To access an element you need to convert it to a list
    print("Third element of nums as list:", list(nums)[2])

if __name__ == "__main__":
    main()
