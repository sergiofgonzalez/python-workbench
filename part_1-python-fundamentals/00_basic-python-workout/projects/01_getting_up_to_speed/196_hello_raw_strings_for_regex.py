"""Illustrates how raw strings simplify specifying regex patterns."""

import re


def main() -> None:
    """Application entry point."""
    # we intend to find matches for \\task
    regular_regex_str = "\\\task"
    raw_regex_str = r"\task"

    print(f"regular string: {regular_regex_str}")
    print(f"raw string: {raw_regex_str}")


if __name__ == "__main__":
    main()
