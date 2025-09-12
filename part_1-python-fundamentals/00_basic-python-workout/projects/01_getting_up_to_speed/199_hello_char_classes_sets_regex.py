"""Illustrates regex character classes and sets."""

import re


def main() -> None:
    """Application entry point."""
    text = "#1$wm_ M\t"
    regex_patterns = [
        r"\d",  # Digit
        r"\D",  # Non-digit
        r"\s",  # Whitespace
        r"\S",  # Non-whitespace
        r"\w",  # Word character (alphanumeric + underscore)
        r"\W",  # Non-word character
        r".",  # Any character except newline
        r"[lmn]",  # Any of the characters l, m, or n
    ]
    print("Text to search:", repr(text))
    max_len = max(len(p) for p in regex_patterns)
    for regex_pattern in regex_patterns:
        matches = re.findall(regex_pattern, text)
        print(f"{regex_pattern:<{max_len}} ==> Matches: {matches}")


if __name__ == "__main__":
    main()
