"""Illustrates how to remove double quotes from a list of strings."""


def main() -> None:
    """Application entry point."""
    x = ['"abc"', 'def', '"ghi"', '"klm"', 'nop']  # noqa: Q000
    x = [item.replace('"', '') for item in x]  # noqa: Q000
    print(x)

if __name__ == "__main__":
    main()
