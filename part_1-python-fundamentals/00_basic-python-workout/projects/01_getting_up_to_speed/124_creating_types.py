"""Illustrate how to create types (type alias) to simplify annotations."""

NestedList = list[list[int]]  # A type alias for a nested list of integers


def main() -> None:
    """Application entry point."""
    my_super_list: NestedList = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(my_super_list)  # Should print [[1, 2, 3],


if __name__ == "__main__":
    main()
