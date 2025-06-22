"""Illustrate the use of b-strings to get the bytes out of strings."""


def main() -> None:
    """Application entry point."""
    str1 = "Hello ABC abc 123"
    print(f"String: {str1}")
    bstr = b"Hello ABC abc 123"
    print(f"Byte string: {bstr}")

    for c in bstr:
        print(f"Character: {c} - {chr(c)}")

    # Getting the bytes in a list comprehension
    byte_list = list(bstr)
    print(f"Byte list: {byte_list}")


if __name__ == "__main__":
    main()
