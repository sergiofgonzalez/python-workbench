"""Illustrate the behavior of defaultdict: a better alternative to setdefault."""

from collections import defaultdict


def main() -> None:
    """Application entry point."""
    eng_to_french = defaultdict(
        lambda: "unknown",
        {"red": "rouge", "green": "vert", "blue": "bleu"},
    )
    print(f"Initial dictionary: {eng_to_french}")

    # defaultdict behaves like a regular dict for existing keys
    assert eng_to_french["red"] == "rouge"
    assert eng_to_french["green"] == "vert"
    assert eng_to_french["blue"] == "bleu"
    print(f"Initial dictionary: {eng_to_french}")

    # Accessing a non-existing key returns the default value and adds the key
    assert eng_to_french["yellow"] == "unknown"
    print(f"After accessing non-existing key 'yellow': {eng_to_french}")
    print("=" * 40)


if __name__ == "__main__":
    main()
