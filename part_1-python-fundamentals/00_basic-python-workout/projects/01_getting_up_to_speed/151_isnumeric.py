"""Illustrate the behavior of isnumeric."""


def main() -> None:
    """Application entry point."""
    age = input("Enter your age: ")
    if age.isnumeric():
        print(f"Your age is {age}.")
    else:
        print("Please enter a valid numeric age.")

    examples = ["123", "45.67", "12e3", "-123"]
    for example in examples:
        print(f"{example}: {example.isnumeric()}")


if __name__ == "__main__":
    main()
