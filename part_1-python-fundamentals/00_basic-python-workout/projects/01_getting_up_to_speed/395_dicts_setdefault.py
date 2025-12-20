"""Illustrate the behavior of dict.setdefault()."""


def main() -> None:
    """Application entry point."""
    eng_to_french = {"red": "rouge", "green": "vert", "blue": "bleu"}

    print(f"Initial dictionary: {eng_to_french}")

    # Using setdefault for an existing key
    french_red = eng_to_french.setdefault("red", "rouge_new")
    print(f"After setdefault on existing key 'red': {eng_to_french}")
    print(f"Returned value for 'red': {french_red}")

    # Using setdefault for a new key
    french_yellow = eng_to_french.setdefault("yellow", "jaune")
    print(f"After setdefault on new key 'yellow': {eng_to_french}")
    print(f"Returned value for 'yellow': {french_yellow}")

    print(f"Final dictionary: {eng_to_french}")


if __name__ == "__main__":
    main()
