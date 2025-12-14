"""Illustrates some basics of lists."""


def main() -> None:
    """Application entry point."""
    print(len([1, 2] * 3))  # 6

    # in doesn't raise an exception if the element is not found
    assert 2 in [1, 2, 3]  # noqa: PLR2004
    assert 4 not in [1, 2, 3]  # noqa: PLR2004

    # index raises a ValueError if the element is not found
    assert [1, 2, 3].index(2) == 1
    try:
        [1, 2, 3].index(4)
    except ValueError as exc:
        print(f"Caught expected exception: {exc}")

    # Which one will raise an exception?
    print("1.")
    try:
        min(["a", "b", "c"])
    except Exception as exc:  # noqa: BLE001
        print(f"Caught unexpected exception: {exc}")

    print("2.")
    try:
        max([1, 2, "three"])
    except Exception as exc:  # noqa: BLE001
        print(f"Caught unexpected exception: {exc}")

    print("3.")
    try:
        [1, 2, 3].count("one") # type: ignore  # noqa: PGH003
    except Exception as exc:  # noqa: BLE001
        print(f"Caught unexpected exception: {exc}")


if __name__ == "__main__":
    main()
