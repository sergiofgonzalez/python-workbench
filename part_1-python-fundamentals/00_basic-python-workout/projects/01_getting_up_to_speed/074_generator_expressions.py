"""Illustrate the syntax of generator expressions/generator comprehensions."""


def main() -> None:
    """Application entry point."""
    squares = (x * x for x in range(10))
    print(f"Squares: {squares}")

    squares = (x * x for x in range(1_000_000))
    for _ in range(10):
        print(next(squares))


if __name__ == "__main__":
    main()
