"""Simple function that calculates the square of a number."""

def square(number: float) -> float:
    """Return the square of the given number."""
    return number * number


def main() -> None:
    """Application entry point."""
    num = 5.0
    result = square(num)
    assert result == 25.0, f"Expected 25.0, got {result}"  # noqa: PLR2004

if __name__ == "__main__":
    main()
