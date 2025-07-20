"""Illustrate how to cast strings into numbers."""


def main() -> None:
    """Application entry point."""
    num = input("Enter a number: ")
    try:
        number = int(num)
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
    else:
        print(f"You entered the number: {number}")


if __name__ == "__main__":
    main()
