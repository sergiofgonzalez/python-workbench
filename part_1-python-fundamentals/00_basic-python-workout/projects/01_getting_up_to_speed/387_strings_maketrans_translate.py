"""Illustrate the use of maketrans and translate for translating strings."""


import string


def main() -> None:
    """Application entry point."""
    s = "IF YOU DON'T CLAIM YOUR HUMANITY, YOU WILL BECOME A STATISTIC."
    translation_table = str.maketrans("AISEO", "41530")
    translated_s = s.translate(translation_table)
    print(f"Original string: {s}")
    print(f"Translated string: {translated_s}")

    # You can bend the rules further and use translation tables
    # to remove characters by mapping them to None.
    remove_punctuation_table = str.maketrans("", "", string.punctuation)
    no_punctuation_s = s.translate(remove_punctuation_table)
    print(f"String without punctuation: {no_punctuation_s}")

if __name__ == "__main__":
    main()
