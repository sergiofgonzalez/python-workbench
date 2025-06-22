"""Illustrate the use of `in` to check if an item belongs to a list."""


def main() -> None:
    """Application entry point."""
    l1 = ["one", 2, "a", False]
    assert "foo" not in l1
    assert "a" in l1


if __name__ == "__main__":
    main()
