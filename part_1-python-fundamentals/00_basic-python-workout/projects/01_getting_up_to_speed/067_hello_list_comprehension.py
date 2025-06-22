"""Illustrate the basics of list comprehensions."""


def main() -> None:
    """Application entry point."""
    # Cubes from 0 to 9 using an imperative approach
    cubes = []
    for num in range(10):
        cubes.append(num**3)  # noqa: PERF401
    print(f"Cubes (imperative): {cubes}")

    # Cubes from 0 to 9 using a list comprehension
    cubes_comp = [num**3 for num in range(10)]
    print(f"Cubes (comprehension): {cubes_comp}")


if __name__ == "__main__":
    main()
