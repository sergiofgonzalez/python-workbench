"""Illustrate defaultdict with a lambda function."""

from collections import defaultdict


def main() -> None:
    """Application entry point."""
    animals = defaultdict(lambda: "Monkey")

    # it works like a regular dict
    animals["Sam"] = "Tiger"
    print(animals)
    print(animals["Sam"])
    print("-" * 40)

    # but it will return "Monkey" for keys not available in the default dict
    print(animals["Joe"])


if __name__ == "__main__":
    main()
