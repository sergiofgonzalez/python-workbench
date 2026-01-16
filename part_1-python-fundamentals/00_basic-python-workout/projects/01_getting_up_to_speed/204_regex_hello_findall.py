"""Illustrate the use of findall to find all the matches in a string."""

import re


def main() -> None:
    """Application entry point."""
    test_str = "hi hey hello"
    # Because there's no grouping, findall() returns the full matches
    # ["hey", "hel"]  # noqa: ERA001
    regex_pattern = r"h[ie]\w"
    matches = re.findall(regex_pattern, test_str)
    if matches:
        print("Matches found!")
        print(matches)
        print(f"Number of matches: {len(matches)}")
    else:
        print(f"No matches found: {regex_pattern=}; {test_str=}.")

    print("===" * 20)
    test_str = "Hey hello"
    # Because there is grouping, findall() returns only the groups
    # [('H', 'e'), ('h', 'e')]  # noqa: ERA001
    regex_pattern = r"(h|H)(i|e)"
    matches = re.findall(regex_pattern, test_str)
    if matches:
        print("Matches found!")
        print(matches)
    else:
        print(f"No matches found: {regex_pattern=}; {test_str=}.")


    print("===" * 20)
    test_str = "hi Hey hello"
    regex_pattern = r"([hH])"
    matches = re.findall(regex_pattern, test_str)
    if matches:
        print("Matches found!")
        print(matches) # see how no tuples are used as there's a single group
    else:
        print(f"No matches found: {regex_pattern=}; {test_str=}.")


if __name__ == "__main__":
    main()
