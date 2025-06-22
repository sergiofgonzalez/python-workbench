"""Illustrate old-school string formatting using the format() function."""


def main() -> None:
    """Application entry point."""
    vector = (2, 5)
    print("My favorite vector is: {}".format(vector))  # noqa: UP032

    print("Hello to {} who turns {} tomorrow!".format("Alice", 30))


if __name__ == "__main__":
    main()
