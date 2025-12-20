"""Illustrates dictionary update and merging."""


def main() -> None:
    """Application entry point."""
    dict1 = {1: "One", 2: "Two"}
    dict2 = {0: "Zero", 1: "__one__"}

    dict1.update(dict2)
    assert dict1 == {0: "Zero", 1: "__one__", 2: "Two"}
    print(f"After update, dict1: {dict1}")


if __name__ == "__main__":
    main()
