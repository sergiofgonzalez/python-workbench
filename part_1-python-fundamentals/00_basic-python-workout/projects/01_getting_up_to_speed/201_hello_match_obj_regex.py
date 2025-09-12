"""Illustrate the use of match objects in regex."""

import re


def main() -> None:
    """Application entry point."""
    regex_pattern = r"(\w\d+)"
    test_string = "xyza2b1c3dd"
    match = re.search(regex_pattern, test_string)
    if match:
        print("Match found!")
        print(f"{match.groups()=}, number of matches={len(match.groups())}")
        print(f"{match.group()=}, {match.span()=}, {match.start()=}, {match.end()=}")
        print(f"{match.group(0)=}, {match.span(0)=}, {match.start(0)=}, {match.end(0)=}")  # noqa: E501
        print(f"{match.group(1)=}, {match.span(1)=}, {match.start(1)=}, {match.end(1)=}")  # noqa: E501
    else:
        print(f"No match found: {regex_pattern=}; {test_string=}.")

    print("===" * 20)
    regex_pattern = r"(\w+), (\w+)"
    test_string = "Homework, urgent; today"
    match = re.match(regex_pattern, test_string)
    if match:
        print("Match found!")
        print(f"{match.groups()=}, number of matches={len(match.groups())}")
        print(f"{match.group()=}, {match.span()=}, {match.start()=}, {match.end()=}")
        for i in range(len(match.groups()) + 1):
            print(f"{i}: {match.group(i)=}, {match.span(i)=}, {match.start(i)=}, {match.end(i)=}")  # noqa: E501
    else:
        print(f"No match found: {regex_pattern=}; {test_string=}.")


if __name__ == "__main__":
    main()
