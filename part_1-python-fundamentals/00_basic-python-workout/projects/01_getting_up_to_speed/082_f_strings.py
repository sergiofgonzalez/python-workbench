"""Illustrate the modern way of string formatting using f-strings."""

def main() -> None:
    """Application entry point."""
    vector = (2, 5)
    print(f"My favorite vector is: {vector}")

    name = "Alice"
    age = 30
    print(f"Hello to {name} who turns {age} tomorrow!")


if __name__ == "__main__":
    main()
