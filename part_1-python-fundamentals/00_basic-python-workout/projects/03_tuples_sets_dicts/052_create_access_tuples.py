"""Creating and accessing tuples in Python."""


def main() -> None:
    """Application entry point."""
    tuple1 = (1, 2)
    tuple2 = ("a", "b", "c", "d")
    tuple3 = 1, 2, 3, 4, 5

    print("First element of tuple1:", tuple1[0])
    print("Second element of tuple1:", tuple1[1])

    print("Element before last in tuple2:", tuple2[-2])
    print("Last element of tuple2:", tuple2[-1])

    print("tuple containing 2nd through 4th elements of tuple3:", tuple3[1:4])


if __name__ == "__main__":
    main()
