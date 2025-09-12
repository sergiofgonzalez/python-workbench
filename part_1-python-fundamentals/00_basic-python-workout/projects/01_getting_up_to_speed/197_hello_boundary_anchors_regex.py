"""Illustrate the use of boundary anchors in regular expressions."""

import re


def main() -> None:
    """Application entry point."""
    print(re.search("^hi", "hi, Python!"))
    print(re.search("task$", "Complete the task"))
    print(re.search(r"^hi task$", "hi task"))
    print(re.search(r"^hi task$", "hi Python task"))


if __name__ == "__main__":
    main()
