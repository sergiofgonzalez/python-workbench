"""Illustrate how to use *_ to ignore positional parameters."""


def foo(*_: str) -> None:
    """Ignore all positional parameters in this dummy function."""
    print("This function ignores all positional parameters.")


def main() -> None:
    """Application entry point."""
    foo("Hello", "World", "This", "is", "ignored")
    print("Function executed successfully.")

    # Trying to pass keyword arguments will fail
    try:
        foo(a="This", b="is", c="not ignored")  # pyright: ignore[reportCallIssue]
    except TypeError as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
