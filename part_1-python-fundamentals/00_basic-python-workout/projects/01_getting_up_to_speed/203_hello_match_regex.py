"""Illustrate the use of the match() to find a match at the start of a string."""

import re


def main() -> None:
    """Application entry point."""
    test_str = "ab12xy34st4ou"
    regex_pattern = r"(\d+)"
    # note that match() finds a match only at the start of the string
    match = re.match(regex_pattern, test_str)
    if match:
        print("Match found!")
        print(match)
    else:
        print(f"No match found: {regex_pattern=}; {test_str=}.")

    print("===" * 20)
    test_str = "12abxy"
    regex_pattern = r"\d+"
    match = re.match(regex_pattern, test_str)
    if match:
        print("Match found!")
        print(match)
    else:
        print(f"No match found: {regex_pattern=}; {test_str=}.")


if __name__ == "__main__":
    main()
