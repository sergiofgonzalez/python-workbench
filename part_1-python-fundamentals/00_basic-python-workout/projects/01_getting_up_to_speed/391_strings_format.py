"""Illustrates the use of str.format()."""


def main() -> None:
    """Application entry point."""
    # you can use both positional and named placeholders
    s = "{0} is the food of {users[1]}".format(
        "Ambrosia",
        users=["the mortals", "the gods"],
    )
    print(s)

    # Using some format specifications
    s = "{0:10} is the food of the gods".format("Ambrosia")  # noqa: UP030
    print(s)

    # The width can also be specified dynamically
    s = "{0:{width}} is the food of the gods".format("Ambrosia", width=10)
    print(s)

    # It also works with named placeholders
    s = "{food:{width}} is the food of the gods".format(food="Ambrosia", width=10)
    print(s)

    # And you can also use the position of the string
    s = "{food:>{width}} is the food of the gods".format(food="Ambrosia", width=10)
    print(s)
    s = "{food:^{width}} is the food of the gods".format(food="Ambrosia", width=10)
    print(s)

    # And even the character that sets the alignment can be dynamic
    s = "{food:{fill}{align}{width}} is the food of the gods".format(
        food="Ambrosia",
        fill="*",
        align="^",
        width=10,
    )
    print(s)

    # Some other examples
    x = "{1:{0}}".format(3, 4)
    print("0----5----0")
    print(repr(x))

    x = "{0:$>5}".format(3)  # noqa: UP030, UP032
    print(repr(x))

    x = "{a:{b}}".format(a=1, b=5)
    print(repr(x))

    x = "{a:{b}}:{0:$>5}".format(3, 4, a=1, b=5, c=10)  # noqa: F522, F523
    print(repr(x))

if __name__ == "__main__":
    main()
