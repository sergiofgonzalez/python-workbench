"""Illustrates more unpacking scenarios."""


def main() -> None:
    """Application entry point."""
    friends = [("jane", 21), ("john", 32), ("jill", 45), ("jack", 23)]

    # Unpacking tuples in a list using indexing
    jacks_name, jacks_age = friends[-1]
    assert jacks_name == "jack"
    assert jacks_age == 23  # noqa: PLR2004
    print(f"Hello to {jacks_name!r} who turns {jacks_age} today!")

    # Unpacking tuples in a list using unpacking
    *_, jack = friends
    jacks_name, jacks_age = jack
    assert jacks_name == "jack"
    assert jacks_age == 23  # noqa: PLR2004
    print(f"Hello to {jacks_name!r} who turns {jacks_age} today!")


if __name__ == "__main__":
    main()
