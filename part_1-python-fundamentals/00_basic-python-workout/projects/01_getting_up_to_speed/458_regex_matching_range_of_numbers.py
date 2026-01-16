"""Matching range of numbers using regular expressions."""

import re


def main() -> None:
    """Application entry point."""
    for number in range(-9, 10):
        number_str = str(number)
        if re.match(r"^[-+]?[0-5]$", number_str):
            print(f"Matched: {number_str} matched the range -5 to 5")
        else:
            print(f"Did not match: {number_str} the range -5 to 5")


if __name__ == "__main__":
    main()
