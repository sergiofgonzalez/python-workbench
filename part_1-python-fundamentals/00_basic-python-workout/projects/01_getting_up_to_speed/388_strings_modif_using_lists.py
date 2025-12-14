"""Illustrates modifying strings using lists."""


import string


def main() -> None:
    """Application entry point."""
    s = (
        "Fairy tales don't tell children that dragons exist: They already know "
        "that! They tell children that dragons can be defeated."
    )
    s_chars = list(s)
    for i, char in enumerate(s_chars):
        if char in string.punctuation:
            s_chars[i] = " "
    modified_s = "".join(s_chars)
    print(f"Original string: {s}")
    print(f"Modified string: {modified_s}")

    # Using translation table is quicker and more succinct
    translation_table = str.maketrans(string.punctuation, " " * len(string.punctuation))
    modified_s_via_translate = s.translate(translation_table)
    print(f"Modified string via translate: {modified_s_via_translate}")

    assert modified_s == modified_s_via_translate

if __name__ == "__main__":
    main()
