"""Illustrate how to concatenate lists."""


def main() -> None:
    """Application entry point."""
    l1 = [1, 2, 3]
    l2 = [4, 5, 6]

    # Concatenating lists using the `+` operator
    l3 = l1 + l2
    print(f"Concatenated list: {l3}")
    assert l3 == [1, 2, 3, 4, 5, 6]

if __name__ == "__main__":
    main()
