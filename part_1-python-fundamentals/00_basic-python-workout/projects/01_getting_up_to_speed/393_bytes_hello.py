"""Illustrates the basics of bytes."""


def main() -> None:
    """Application entry point."""
    s = "\N{LATIN SMALL LETTER A WITH ACUTE}"
    print(s)

    b = s.encode("utf-8")
    print(b)

    try:
        b += "a" # type: ignore  # noqa: PGH003
    except TypeError as e:
        print(f"Caught expected exception: {e}")

    # using encode is unnecessary for simple ASCII bytes
    regular_a_bytes = "a".encode("utf-8")  # noqa: UP012
    print(regular_a_bytes)

    # This is more pythonic
    regular_a_bytes = b"a"
    print(regular_a_bytes)

    combined_bytes = b + regular_a_bytes
    print(combined_bytes)

    combined_string = combined_bytes.decode("utf-8")
    print(combined_string)

if __name__ == "__main__":
    main()
