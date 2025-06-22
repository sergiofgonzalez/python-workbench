"""Illustrate how to escape curly braces in Python f-strings."""

def main() -> None:
    """Application entry point."""
    obj = {"name": "Vacuum Cleaner", "price": 130.675}

    # Printing "Vaccuum Cleaner: {130.675}"
    print(f"{obj['name']}: {{{obj['price']}}}")


if __name__ == "__main__":
    main()
