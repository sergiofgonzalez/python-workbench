"""Illustrate how to annotate dicts."""


def main() -> None:
    """Application entry point."""
    my_dict: dict[str, int] = {"Alice": 30, "Bob": 25, "Charlie": 35}
    print(my_dict)  # Should print {'Alice': 30, 'Bob': 25, 'Charlie': 35}


if __name__ == "__main__":
    main()
