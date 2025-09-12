"""Illustrate the use of nonlocal in Python."""


def say_hello() -> None:
    """Demonstrate nonlocal variable usage."""
    name = "Charlize"

    def read_name() -> str:
        """Illustrate how nonlocal isn't required to read a var in enclosing scope."""
        print(f"Current name: {name}")
        return name

    def update_name() -> str:
        """Illustrate how nonlocal is required to modify a var in enclosing scope."""
        nonlocal name
        print(f"Original name: {name}")
        name += " Theron"
        return name

    print("Before update:")
    print(read_name())
    message = update_name()
    print(message)


def main() -> None:
    """Application entry point."""
    say_hello()


if __name__ == "__main__":
    main()
