"""Illustrates the use of informal DocStrings."""


def greet_me(name: str) -> None:
    """Greet the user by name.

    Simple function to that receives a name and prints a greeting, that is documented
    using an informal docstring.
    """
    print(f"Hello, {name}!")


def main() -> None:
    """Application entry point."""
    greet_me("Alice")


if __name__ == "__main__":
    main()
