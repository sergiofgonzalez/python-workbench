"""Finding the first match in a list or iterable using `index()`."""


def main() -> None:
    """Application entry point."""
    friends = ["Linda", "Tiffany", "Florina", "Jovann"]

    # Finding the first friend whose name length is 7
    friends_length = [len(friend) for friend in friends]
    length_first_match = friends_length.index(7)
    print(f"Index of first match: {length_first_match}")
    assert length_first_match == 1

    first_match = friends[length_first_match]
    print(f"First match: {first_match}")
    assert first_match == "Tiffany"


if __name__ == "__main__":
    main()
