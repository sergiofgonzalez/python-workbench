"""Illustrate the use of isalpha."""


def main() -> None:
    """Application entry point."""
    examples = [
        "Homework",
        "CS101",
        "Python3",
        "Hello World",
        "Hello_123",
        "123",
        "!@#",
    ]
    for example in examples:
        print(f"{example}: {example.isalpha()}")


if __name__ == "__main__":
    main()
