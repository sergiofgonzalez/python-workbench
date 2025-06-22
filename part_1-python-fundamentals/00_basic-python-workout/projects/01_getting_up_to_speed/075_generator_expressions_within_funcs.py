"""Illustrate the syntax for generator expressions within functions."""


def main() -> None:
    """Application entry point."""
    # Calculate the sum of squares of the first million integers using a generator expression
    squares_sum = sum(x * x for x in range(1, 1_000_001))
    print(f"Sum of squares: {squares_sum}")


if __name__ == "__main__":
    main()
