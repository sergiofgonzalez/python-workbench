"""Illustrate set operations."""


def main() -> None:
    """Application entry point."""
    a = {1, 2, 3}
    b = {3, 4, 5}
    print("a =", a)
    print("b =", b)
    print("a | b =", a | b)  # union
    print("a & b =", a & b)  # intersection
    print("a ^ b =", a ^ b)  # symmetric difference
    print("a - b =", a - b)  # difference

    # Now with methods
    print(f"{a.union(b)=}")  # union
    print(f"{a.intersection(b)=}")  # intersection
    print(f"{a.symmetric_difference(b)=}")  # symmetric difference
    print(f"{a.difference(b)=}")  # difference


if __name__ == "__main__":
    main()
