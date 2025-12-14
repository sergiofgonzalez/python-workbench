"""String manipulation methods: strip, rstrip, lstrip, removeprefix, removesuffix."""


import string


def main() -> None:
    """Application entry point."""
    # strip, rstrip, lstrip
    s = "  Hello, world!  \t\n"
    assert s.strip() == "Hello, world!"
    assert s.rstrip() == "  Hello, world!"
    assert s.lstrip() == "Hello, world!  \t\n"
    print("=== strip, rstrip, lstrip assertions passed ===")

    # consulting whitespace characters in this platform
    print(f"{string.whitespace=}")

    # consulting punctuation characters in this platform
    print(f"{string.punctuation=}")

    s = "www.python.org"
    assert s.removeprefix("www.") == "python.org"
    assert s.removesuffix(".org") == "www.python"
    print("=== removeprefix, removesuffix assertions passed ===")

    # Using custom strip characters
    s = "(name, date),\n"
    print(f"{s=}: {s.rstrip("),")!r}")   # custom rstrip
    print(f"{s=}: {s.strip("),\n")!r}")  # custom strip
    print(f"{s=}: {s.strip("\n)(,")!r}")  # custom strip
    assert s.strip("\n)(,") == "name, date"
    print("=== custom strip assertions passed ===")

if __name__ == "__main__":
    main()
