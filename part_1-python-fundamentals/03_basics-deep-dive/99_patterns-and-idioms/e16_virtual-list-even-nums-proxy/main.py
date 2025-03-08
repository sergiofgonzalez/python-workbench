"""Main application program."""

from even_numbers import even_numbers


def main() -> None:
    """Application entry-point."""
    assert 2 in even_numbers
    assert 5 not in even_numbers
    print(even_numbers[7])
    print("=" * 80)
    for i in range(10):
        print(f"{i}: {even_numbers[i]}")


if __name__ == "__main__":
    main()
