"""Illustrate the use of the specifiers `=` and `!r` in different scenarios."""


def f(n: int) -> int:
    """Return the value passed incremented by 1."""
    return n + 1


def main() -> None:
    """Application entry point."""
    x = 57
    print(f"{x=}")  # Using '=' to show variable name and value

    s = "Hello, World!"
    print(f"{s=}")  # Using '=' to show variable name and value

    # Using '!r' to show the representation of the string
    print(f"{s!r}")  # This will show the string with quotes
    print(f"{x!r}")  # This will NOT show the integer with quotes

    # Using '=' with a function call
    print(f"{f(42)=}")


if __name__ == "__main__":
    main()
