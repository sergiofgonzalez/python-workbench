"""Illustrate the use of search() in regex to find a match anywhere in a string."""

import re


def main() -> None:
    """Application entry point."""
    test_str = "ab12xy34st4ou"
    regex_pattern = r"(\d+)"
    # note that search() finds the first match anywhere in the string
    # but only returns that first match
    match = re.search(regex_pattern, test_str)
    if match:
        print("Match found!")
        print(f"{match.groups()=}, number of matches={len(match.groups())}")
        print(f"{match.group()=}, {match.span()=}, {match.start()=}, {match.end()=}")
        print(
            f"{match.group(1)=}, {match.span(1)=}, {match.start(1)=}, {match.end(1)=}",
        )
    else:
        print(f"No match found: {regex_pattern=}; {test_str=}.")

    print("===" * 20)
    test_str = "12abxy"
    regex_pattern = r"\d+"
    match = re.search(regex_pattern, test_str)
    if match:
        print("Match found!")
        print(match)
        print(f"{match.groups()=}, number of matches={len(match.groups())}")
    else:
        print(f"No match found: {regex_pattern=}; {test_str=}.")

if __name__ == "__main__":
    main()
