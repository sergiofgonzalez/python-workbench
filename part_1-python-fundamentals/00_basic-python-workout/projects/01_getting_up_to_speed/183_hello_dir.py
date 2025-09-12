"""Illustrates the use of `dir()` to get all the methods and attributes of an object."""


def main() -> None:
    """Application entry point."""
    name = "Alice"
    print(dir(name))  # List all attributes and methods of the string object


if __name__ == "__main__":
    main()
