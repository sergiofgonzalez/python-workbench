"""Python variables are labels instead of buckets that store values."""


def print_value_and_id(*args: object) -> None:
    """Print the value and the id of the given variable."""
    for var in args:
        print(f"{var=}, {id(var)=:#x}")


def main() -> None:
    """Application entry point."""
    a = [1, 2, 3]
    b = a
    c = b
    print_value_and_id(a, b, c)
    assert id(a) == id(b) == id(c)
    print("=" * 20)

    b[1] = -5
    print_value_and_id(a, b, c)
    assert id(a) == id(b) == id(c)
    print("=" * 20)

    a = 1
    b = a
    c = b
    print_value_and_id(a, b, c)
    assert id(a) == id(b) == id(c)
    print("=" * 20)
    b = -5
    print_value_and_id(a, b, c)
    assert id(b) != id(a) == id(c)
    print("=" * 20)


if __name__ == "__main__":
    main()
