"""Illustrate how to convert a list of chars into a string using join()."""


def main() -> None:
    """Application entry point."""
    chars = ["a", "b", "c"]
    strings = ["alpha", "beta", "gamma"]
    nums = [1, 2, 3, 4, 5]

    # Converting each list into a single string using join()
    chars_joined = "".join(chars)
    print(f"Chars joined: {chars_joined}")
    assert chars_joined == "abc"

    strings_joined = " ".join(strings)
    print(f"Strings joined: {strings_joined}")
    assert strings_joined == "alpha beta gamma"

    nums_joined = ", ".join(map(str, nums))
    print(f"Nums joined: {nums_joined}")
    assert nums_joined == "1, 2, 3, 4, 5"


if __name__ == "__main__":
    main()
