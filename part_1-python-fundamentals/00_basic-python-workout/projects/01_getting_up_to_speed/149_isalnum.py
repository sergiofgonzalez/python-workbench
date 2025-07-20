"""Illustrate the behavior of isalnum."""


def main() -> None:
    """Application entry point."""
    examples = ["123@!", "123asdf", "Hello123", "Hello 123", "Hello_123", "123", "!@#"]
    for example in examples:
        print(f"{example}: {example.isalnum()}")


if __name__ == "__main__":
    main()
