"""Illustrate how sub() can be used to replace patterns in a string."""

import re


def main() -> None:
    """Application entry point."""
    test_str = "123,456_789"
    regex_pattern = r"\D"
    replacement = "-"
    result = re.sub(regex_pattern, replacement, test_str)
    print("Substitution result:")
    print(result)


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
