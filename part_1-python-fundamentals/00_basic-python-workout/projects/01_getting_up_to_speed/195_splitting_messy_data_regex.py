"""Illustrates the basics of splitting messy text line with regex."""

import re


def main() -> None:
    """Application entry point."""
    text = "field1,field2;field3;field4_field5"
    regex_str = r"[,;_]"  # split on comma, semicolon, or underscore
    fields = re.split(regex_str, text)
    print(f"Split fields: {fields=}")


if __name__ == "__main__":
    main()
