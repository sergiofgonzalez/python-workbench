"""Illustrates how Python favors EAFP via exceptions for regular logic."""


def cell_value(s: str) -> float | None:
    """Convert cell value to a number, 0 if empty, None if invalid."""
    try:
        if s == "":
            return 0
        return float(s)
    except ValueError:
        return None


def main() -> None:
    """Application entry point."""
    test_values = ["42", "", "invalid", "100", "-7", "3.14", "1+2j"]
    for val in test_values:
        result = cell_value(val)
        print(f"cell_value({val!r}) -> {result}")


if __name__ == "__main__":
    main()
