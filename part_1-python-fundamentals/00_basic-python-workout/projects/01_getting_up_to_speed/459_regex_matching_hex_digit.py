"""Illustrate how to match a hexadecimal digit."""

import re


def main() -> None:
    """Application entry point."""
    for char in [chr(i) for i in range(ord("0"), ord("z") + 1)]:
        hex_digit = r"((0x)|(0X))?[0-9a-fA-F]"
        if re.match(hex_digit, char):
            print(f"Matched: {char!r} is a hexadecimal digit")
        else:
            print(f"Did not match: {char!r} is not a hexadecimal digit")


if __name__ == "__main__":
    main()
