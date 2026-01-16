"""Introduce the re module."""

import re


def hello_re_oop() -> None:
    """Demonstrate basic usage of the re module."""
    regex_str = r"do"
    pattern = re.compile(regex_str)
    print(f"Compiled regex pattern: {pattern=}, type={type(pattern).__name__}")

    text = "do homework"
    match = pattern.search(text)
    print(f"Matching pattern in '{text}' yields: {match=}, type={type(match).__name__}")


def hello_re_functional() -> None:
    """Demonstrate functional usage of the re module."""
    regex_str = r"do"
    text = "do homework"
    match = re.search(regex_str, text)
    print(f"Matching pattern in '{text}' yields: {match=}, type={type(match).__name__}")


def main() -> None:
    """Application entry point."""
    hello_re_oop()
    hello_re_functional()


if __name__ == "__main__":
    main()
