"""Basic indexing and slicing with Python strings."""


def main() -> None:
    """Application entry point."""
    name = "foobar"
    assert name[0] == "f"
    assert name[1] == "o"
    assert name[-1] == "r"
    assert name[-2] == "a"
    assert name[0:2] == "fo"
    assert name[3:] == "bar"
    assert name[:2] == "fo"
    assert name[1:-1] == "ooba"


if __name__ == "__main__":
    main()
