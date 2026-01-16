"""Illustrates how raw strings simplify specifying regex patterns."""

import re


def main() -> None:
    """Application entry point."""
    # we intend to find matches for \\task
    regular_regex_str = "\\\task"
    raw_regex_str = r"\task"

    print(f"regular string: {regular_regex_str}")
    print(f"raw string: {raw_regex_str}")
    print("=" * 40)

    # when using raw strings, backslashes are treated literally
    pattern = re.compile(r"\\task")
    src_string = "To activate a task you need to use the \\task command.\n"

    print(f"Source string:\n{src_string}")
    result = pattern.search(src_string)
    print(result)

    # if we don't use raw strings, we need to escape backslashes
    pattern = re.compile("\\\\task")
    result = pattern.search(src_string)
    print(result)


if __name__ == "__main__":
    main()
