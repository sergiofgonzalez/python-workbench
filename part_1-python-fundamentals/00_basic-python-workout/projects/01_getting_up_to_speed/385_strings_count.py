"""Illustrates the string method count."""


def main() -> None:
    """Application entry point."""
    s = "Mississippi"

    # Count the occurrences of "ss"
    count_ss = s.count("ss")
    print(f"The number of occurrences of 'ss' is: {count_ss}")
    assert count_ss == 2  # noqa: PLR2004

    # Count the occurrences of "zz" (not found)
    count_zz = s.count("zz")
    print(f"The number of occurrences of 'zz' is: {count_zz}")
    assert count_zz == 0


if __name__ == "__main__":
    main()
