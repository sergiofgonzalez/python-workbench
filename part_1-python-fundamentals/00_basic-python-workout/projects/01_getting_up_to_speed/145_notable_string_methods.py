"""Illustrate the use of some notable string methods."""


def main() -> None:  # noqa: PLR0915
    """Application entry point."""
    # isalpha() returns True if the string contains only chars and is not empty
    print("=== isalpha() ===")
    print(f"{"".isalpha()=}")
    print(f"{"foo".isalpha()=}")
    print(f"{"foo123".isalpha()=}")

    # isalnum returns True if the string contains characters or digits and is not empty
    print("\n=== isalnum() ===")
    print(f"{"".isalnum()=}")
    print(f"{"foo".isalnum()=}")
    print(f"{"foo123".isalnum()=}")
    print(f"{"foo 123".isalnum()=}")
    print(f"{"foo_123".isalnum()=}")

    # isdecimal() returns True if the string contains only digits and is not empty
    print("\n=== isdecimal() ===")
    print(f"{"".isdecimal()=}")
    print(f"{"123".isdecimal()=}")
    print(f"{"123.45".isdecimal()=}")
    print(f"{"123abc".isdecimal()=}")
    print(f"{"123 45".isdecimal()=}")
    print(f"{"-123".isdecimal()=}")

    # lower() returns a copy of the string with all characters converted to lowercase
    print("\n=== lower() ===")
    print(f"{"".lower()=}")
    print(f"{"FOO".lower()=}")
    print(f"{"Foo".lower()=}")

    # islower() returns True if the string contains only lowercase characters and
    # is not empty
    print("\n=== islower() ===")
    print(f"{"".islower()=}")
    print(f"{"foo".islower()=}")
    print(f"{"Foo".islower()=}")

    # upper() returns a copy of the string with all characters converted to uppercase
    print("\n=== upper() ===")
    print(f"{"".upper()=}")
    print(f"{"foo".upper()=}")
    print(f"{"Foo".upper()=}")

    # isupper() returns True if the string contains only uppercase characters and
    # is not empty
    print("\n=== isupper() ===")
    print(f"{"".isupper()=}")
    print(f"{"FOO".isupper()=}")
    print(f"{"Foo".isupper()=}")

    # title() returns a copy of the string with the first character of each word
    # capitalized
    # Note that it does not handle prepositions or articles correctly
    # (e.g., "for", "a", "of" should not be capitalized
    print("\n=== title() ===")
    print(f"{"".title()=}")
    print(f"{"foo bar".title()=}")
    print(f"{"foo bar baz".title()=}")
    print(f"{"for a fistful of dollars".title()=}")

    # capitalize() returns a copy of the string with the first character capitalized
    print("\n=== capitalize() ===")
    print(f"{"".capitalize()=}")
    print(f"{"foo".capitalize()=}")
    print(f"{"foo bar".capitalize()=}")

    # startswith() returns True if the string starts with the specified prefix
    print("\n=== startswith() ===")
    print(f"{"".startswith("f")=}")
    print(f"{"foo".startswith("f")=}")
    print(f"{"foo".startswith("o")=}")
    print(f"{"foo".startswith("fo")=}")
    print(f"{"foo".startswith("bar")=}")

    # endswith() returns True if the string ends with the specified suffix
    print("\n=== endswith() ===")
    print(f"{"".endswith("f")=}")
    print(f"{"foo".endswith("f")=}")
    print(f"{"foo".endswith("o")=}")
    print(f"{"foo".endswith("fo")=}")
    print(f"{"foo".endswith("bar")=}")

    # find() returns the lowest index of the substring if found, otherwise -1
    print("\n=== find() ===")
    print(f"{"".find("f")=}")
    print(f"{"foo".find("f")=}")
    print(f"{"foo".find("o")=}")
    print(f"{"foo".find("fo")=}")
    print(f"{"foo".find("bar")=}")

    # replace() returns a copy of the string with all occurrences of the
    # old substring replaced by the new substring
    print("\n=== replace() ===")
    print(f"{"".replace("f", "b")=}")
    print(f"{"foo".replace("f", "b")=}")
    print(f"{"foo".replace("o", "a")=}")
    print(f"{"foo".replace("fo", "ba")=}")
    print(f"{"foo".replace("bar", "baz")=}")

    # split() returns a list of substrings separated by the specified separator
    print("\n=== split() ===")
    print(f"{"".split("f")=}")  # noqa: SIM905
    print(f"{"foo".split("f")=}")  # noqa: SIM905
    print(f"{"foo bar".split(" ")=}")  # noqa: SIM905
    print(f"{"foo bar baz".split(" ")=}")  # noqa: SIM905

    # join() returns a string that is the concatenation of the strings in the iterable
    print("\n=== join() ===")
    print(f"{"".join(['f', 'o', 'o'])=}")  # noqa: FLY002
    print(f"{" ".join(['foo', 'bar'])=}")  # noqa: FLY002
    print(f"{' - '.join(['foo', 'bar', 'baz'])=}")  # noqa: FLY002

    # strip() returns a copy of the string with leading and trailing whitespace removed
    print("\n=== strip() ===")
    print(f"{"".strip()=}")
    print(f"{"   foo   ".strip()=}")
    print(f"{"   foo bar   ".strip()=}")


if __name__ == "__main__":
    main()
