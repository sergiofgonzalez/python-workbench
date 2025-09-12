"""Illustrate the use of finditer to get an iterator yielding Match objects."""

import re


def main() -> None:
    """Application entry point."""
    test_str = "hi Hey hello"
    regex_pattern = r"(h|H)(i|e)"
    matches = re.finditer(regex_pattern, test_str)
    if matches:
        print("Matches found!")
        for match in matches:
            print(match)
    else:
        print(f"No matches found: {regex_pattern=}; {test_str=}.")


if __name__ == "__main__":
    main()
