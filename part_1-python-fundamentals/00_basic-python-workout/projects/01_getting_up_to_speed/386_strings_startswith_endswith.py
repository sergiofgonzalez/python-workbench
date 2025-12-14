"""Illustrate the use of startswith and endswith."""


def main() -> None:
    """Application entry point."""
    s = "Mississippi"
    print(f"{s.startswith("Miss")=}")
    print(f"{s.endswith("ippi")=}")
    print(f"{s.startswith("foo")=}")
    print(f"{s.endswith("bar")=}")

if __name__ == "__main__":
    main()
