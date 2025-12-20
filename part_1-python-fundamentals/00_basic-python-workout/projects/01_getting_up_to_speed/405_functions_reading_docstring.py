"""Illustrates how to access the docstring of a function."""


def greet(name: str) -> str:
    """Return a greeting message for the given name.

    Args:
        name (str): The name of the person to greet.

    Returns:
        str: A greeting message.

    """
    return f"Hello, {name}!"


def main() -> None:
    """Application entry point."""
    docstring = greet.__doc__
    print("Docstring of the 'greet' function:")
    print(docstring)


if __name__ == "__main__":
    main()
