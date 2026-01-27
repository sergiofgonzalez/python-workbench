"""Illustrate type checking with type(), isinstance()."""


def fn_requiring_list(data: list[object]) -> None:
    """Print the length of a list of integers."""
    try:
        print(f"Received list with {len(data)} elements.")
    except TypeError:
        print("Error: Provided data does not seem to be a list.")


def main() -> None:
    """Application entry point."""
    # We need to ensure that the variable is of type list
    data = [1, 2, 3]
    if type(data) is list:
        print("data is a list (checked with type())")
    else:
        print("data is NOT a list (checked with type())")

    if isinstance(data, list):
        print("data is a list (checked with isinstance())")
    else:
        print("data is NOT a list (checked with isinstance())")

    # You can also rely on duck typing
    if hasattr(data, "__len__"):
        print("data has __len__ attribute (duck typing)")
    else:
        print("data does NOT have __len__ attribute (duck typing)")

    if hasattr(55, "__len__"):
        print("data has __len__ attribute (duck typing)")
    else:
        print("data does NOT have __len__ attribute (duck typing)")

    # EAFP - Easier to Ask Forgiveness than Permission
    fn_requiring_list(data)
    fn_requiring_list(55)  # ty:ignore[invalid-argument-type]


if __name__ == "__main__":
    main()
