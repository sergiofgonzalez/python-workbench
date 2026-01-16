"""Illustrate the use of split with regex."""

import re


def main() -> None:
    """Application entry point."""
    test_str = "a1b2c3d4e"
    regex_pattern = r"\d+"
    result = re.split(regex_pattern, test_str)
    print("Split result:")
    print(result)


if __name__ == "__main__":
    main()
