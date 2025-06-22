"""Illustrate how to create a dictionary using literals."""


def main() -> None:
    """Application entry point."""
    dog = {
        "name": "Mara",
        "age": 7,
    }

    print(f"My favorite dog is {dog['name']} and it is {dog['age']} years old.")


if __name__ == "__main__":
    main()
