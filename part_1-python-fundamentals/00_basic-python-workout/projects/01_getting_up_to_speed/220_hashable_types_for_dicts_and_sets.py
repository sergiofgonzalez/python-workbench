"""Introduces the hashable types required for dict keys and sets."""


def main() -> None:
    """Application entry point."""
    try:
        my_dict = {[1, 2, 3]: "a list as a key"}  # type: ignore  # noqa: F841, PGH003
    except TypeError as err:
        print("Error trying to use a list as a dict key:", err)

    try:
        my_set = {{"a": 0}}  # type: ignore  # noqa: F841, PGH003
    except TypeError as err:
        print("Error trying to use a dict as a set element:", err)


if __name__ == "__main__":
    main()
