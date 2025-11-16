"""Illustrate how to create a list of letters from a string."""


def main() -> None:
    """Application entry point."""
    str_value = "ABCDE"
    letters = list(str_value)
    assert letters == ["A", "B", "C", "D", "E"]
    print("=== PASSED ===")


if __name__ == "__main__":
    main()
