"""Illustrate the different ways to add elements to a list."""


def main() -> None:
    """Application entry point."""
    items = []

    # Adding elements using append
    items.append("one")
    print(f"List after append: {items}")
    assert items == ["one"]

    # Adding a second element using append
    items.append("two")
    print(f"List after second append: {items}")
    assert items == ["one", "two"]

    # Adding an element using extend
    items.extend(["three"])
    assert items == ["one", "two", "three"]

    # Adding multiple elements using extend
    items.extend(["four", "five"])
    assert items == ["one", "two", "three", "four", "five"]

    # Adding an element using +=
    items += ["six"]
    assert items == ["one", "two", "three", "four", "five", "six"]

    # Adding three elements using +=
    items += ["seven", "eight", "nine"]
    assert items == [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
    print(f"List after +=: {items}")

    # Creating a new list by combining two lists using +
    nums = [1, 2, 3] + [4, 5, 6, 7, 8]  # noqa: RUF005
    assert nums == [1, 2, 3, 4, 5, 6, 7, 8]

    # Using insert to add an element at the front
    nums.insert(0, 0)
    assert nums == [0, 1, 2, 3, 4, 5, 6, 7, 8]

    # Using insert to add an element at a specific position
    nums.insert(4, 3.5)  # type: ignore  # noqa: PGH003
    assert nums == [0, 1, 2, 3, 3.5, 4, 5, 6, 7, 8]
    print(f"Final list: {nums}")


if __name__ == "__main__":
    main()
