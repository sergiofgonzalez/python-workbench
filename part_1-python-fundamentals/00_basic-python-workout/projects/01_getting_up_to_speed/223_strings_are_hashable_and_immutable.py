"""Illustrates that Python strings are hashable and immutable."""


def main() -> None:
    """Application entry point."""
    my_string = "Hello, world!"
    print(f"{my_string=}")
    print(f"0x{id(my_string):x=} {hash(my_string)=}")

    try:
        my_string[0] = "h" # type: ignore  # noqa: PGH003
    except Exception as err:  # noqa: BLE001
        print(f"Error trying to modify a string: {err} (type: {type(err).__name__})")

    another_string = my_string.replace("H", "h")
    print(f"{another_string=}")
    print(f"0x{id(my_string):x=} {hash(my_string)=}")
    print(f"0x{id(another_string):x=} {hash(another_string)=}")

    # another way of replacing just the first character
    yet_another_string = "h" + my_string[1:]
    print(f"{yet_another_string=}")
    print(f"0x{id(my_string):x=} {hash(my_string)=}")
    print(f"0x{id(yet_another_string):x=} {hash(yet_another_string)=}")


if __name__ == "__main__":
    main()
