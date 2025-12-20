"""A simple generator expressions example."""

def main() -> None:
    """Application entry point."""
    x = [1, 2, 3, 4, 5]
    squared = (n * n for n in x)
    for value in squared:
        print(value)

    materialized_squared = list(squared)
    assert materialized_squared == []  # already exhausted

    squared2 = (n * n for n in x)
    materialized_squared2 = list(squared2)
    assert materialized_squared2 == [1, 4, 9, 16, 25]


if __name__ == "__main__":
    main()
