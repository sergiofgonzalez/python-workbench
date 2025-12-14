"""Illustrates the string methods find and rfind."""


def main() -> None:
    """Application entry point."""
    s = "Mississippi"

    # Find the first occurrence of "ss"
    first_ss = s.find("ss")
    print(f"The first occurrence of 'ss' is at index: {first_ss}")
    assert first_ss == 2  # noqa: PLR2004

    # Find the first occurrence of "zz" (not found)
    first_zz = s.find("zz")
    print(f"The first occurrence of 'zz' is at index: {first_zz}")
    assert first_zz == -1

    # Find the first occurrence of "ss" ignoring the first 2 characters
    first_ss_after_2 = s.find("ss", 2)
    print(f"The first occurrence of 'ss' after index 2 is at index: {first_ss_after_2}")
    assert first_ss_after_2 == 2  # noqa: PLR2004

    # Find the first occurrence of "ss" ignoring all characters before pos 3
    first_ss_after_3 = s.find("ss", 3)
    print(f"The first occurrence of 'ss' after index 3 is at index: {first_ss_after_3}")
    assert first_ss_after_3 == 5  # noqa: PLR2004

    # Find the first occurrence of "ss" ignoring the first chactert and
    # ignoring all the characters at or after pos 4th
    first_ss_1_4 = s.find("ss", 1, 4)
    print(
        f"First occurrence of 'ss' between index 1 and 4 is at index: {first_ss_1_4}",
    )
    assert first_ss_1_4 == 2  # noqa: PLR2004

    # Find the first occurrence of "ss" ignoring the first 4 characters when
    # starting from the end of the string
    last_ss_after_4 = s.rfind("ss", 4)
    print(f"The last occurrence of 'ss' after index 4 is at index: {last_ss_after_4}")
    assert last_ss_after_4 == 5  # noqa: PLR2004


if __name__ == "__main__":
    main()
