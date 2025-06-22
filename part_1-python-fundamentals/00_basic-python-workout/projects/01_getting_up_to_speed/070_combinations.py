"""Create a combination of elements using list comprehensions and tuples."""


def main() -> None:
    """Application entry point."""
    combo = [(x, y) for x in range(-1, 6) for y in range(2)]
    print(f"Combo: {combo}")


if __name__ == "__main__":
    main()
