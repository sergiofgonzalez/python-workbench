"""Illustrate the use of regex logical operators."""

import re


def main() -> None:
    """Application entry point."""
    print(re.findall(r"a|b", "a c d d b ab"))  # Matches 'a' or 'b'
    print(re.findall(r"a|b", "c d d b"))  # Matches 'b'
    print(re.findall(r"(abc)", "ab bc abc ac"))  # Matches 'abc'
    print(re.findall(r"abc", "ab bc abc ac"))  # Matches 'abc'
    print(re.findall(r"[^a]", "abcde"))  # Matches any character except 'a'


if __name__ == "__main__":
    main()
