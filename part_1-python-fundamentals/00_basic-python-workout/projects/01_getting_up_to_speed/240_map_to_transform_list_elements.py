"""Illustrate how to use map to transform the elements of a string."""


def main() -> None:
    """Application entry point."""
    nums_as_str = ["1.23", "4.56", "7.89"]
    nums_as_floats = list(map(float, nums_as_str))
    assert nums_as_floats == [1.23, 4.56, 7.89]
    print("=== PASSED ===")


if __name__ == "__main__":
    main()
