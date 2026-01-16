"""Illustrate the use of quantifiers in regular expressions."""

import re


def main() -> None:
    """Application entry point."""
    text_str = "h hi hii hiii hiiii"
    regex_patterns = [
        "hi?",
        "hi*",
        "hi+",
        "hi{3}",
        "hi{2,3}",
        "hi{2,}",
        "hi??",
        "hi*?",
        "hi+?",
        "hi{2,}?",
    ]
    max_len = max(len(p) for p in regex_patterns)
    for regex_pattern in regex_patterns:
        print(f"{regex_pattern:<{max_len}} ==> {re.findall(regex_pattern, text_str)=}")


if __name__ == "__main__":
    main()
