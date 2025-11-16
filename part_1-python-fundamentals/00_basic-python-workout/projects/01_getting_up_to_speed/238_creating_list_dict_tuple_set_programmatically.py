"""Illustrate how to create lists, dictionaries, tuples, and sets programmatically."""


def main() -> None:
    """Application entry point."""
    numbers = list(range(10))
    assert numbers == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("=== PASSED ===")

    some_tuples = [("one", 1), ("two", 2), ("three", 3)]
    numbers_by_name = dict(some_tuples)
    assert numbers_by_name == {"one": 1, "two": 2, "three": 3}
    print("=== PASSED ===")

    some_random_nums = (1, 2, 4, 2, 5, 3, 4, 6, 7, 1, 2, 5)
    distinct_nums = set(some_random_nums)
    assert distinct_nums == {1, 2, 3, 4, 5, 6, 7}
    print("=== PASSED ===")


if __name__ == "__main__":
    main()
