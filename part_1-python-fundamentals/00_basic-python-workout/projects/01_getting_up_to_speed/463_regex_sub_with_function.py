"""Illustrate how to make substitutions in a string with sub()."""

import re


def int_to_float(match: re.Match) -> str:
    """Convert an integer string to a float string by adding .0."""
    int_str = match.group("int_number")
    return f"{int_str}.0"


def main() -> None:
    """Application entry point."""
    test_str = "1, 2, 3 count with me, that's how the numbers go 4, 5, 6, 7, 8, 9!"
    pattern = re.compile(r"(?P<int_number>\d+)")
    result = pattern.sub(int_to_float, test_str)
    print(f"Original string: {test_str}")
    print(f"Modified string: {result}")


if __name__ == "__main__":
    main()
