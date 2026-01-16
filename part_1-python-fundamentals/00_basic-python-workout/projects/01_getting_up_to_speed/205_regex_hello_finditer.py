"""Illustrate the use of finditer to get an iterator yielding Match objects."""

import re


def main() -> None:
    """Application entry point."""
    test_str = "hi Hey hello"
    regex_pattern = r"(h|H)(i|e)"

    # 1. using next()
    matches = re.finditer(regex_pattern, test_str)
    if matches:
        print("Matches found!")
        first_match = next(matches)
        print(first_match)
        second_match = next(matches)
        print(second_match)
        third_match = next(matches)
        print(third_match)
        try:
            fourth_match = next(matches)
            print(fourth_match)
        except StopIteration:
            print("No more matches.")
    else:
        print(f"No matches found: {regex_pattern=}; {test_str=}.")
    print("=" * 40)

    # 2. using list()
    # 3. using for
    matches = re.finditer(regex_pattern, test_str)
    if matches:
        print("Matches found!")
        match_list = list(matches)
        print(match_list)
    else:
        print(f"No matches found: {regex_pattern=}; {test_str=}.")
    print("=" * 40)

    # 3. using for
    matches = re.finditer(regex_pattern, test_str)
    if matches:
        print("Matches found!")
        for match in matches:
            print(match)
    else:
        print(f"No matches found: {regex_pattern=}; {test_str=}.")
    print("=" * 40)


if __name__ == "__main__":
    main()
