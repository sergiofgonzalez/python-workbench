"""Illustrate how to use regex to extract delimited data from a one line string."""

import re


def main() -> None:
    """Application entry point."""
    # because we want to get only the list of fields, we can use a very simple
    # regex pattern that matches only the alphanumeric characters
    # and ignores the delimiters (underscores and commas)
    # Also: re.findall() returns all non-overlapping captured groups which is
    # exactly what we need.

    text_line = "fld1_,fld2__,fld3,,__fld4_,_fld5"
    regex_pattern = r"([a-z0-9]+)"
    matches = re.findall(regex_pattern, text_line)
    print(matches)
    assert matches == ["fld1", "fld2", "fld3", "fld4", "fld5"]


if __name__ == "__main__":
    main()
