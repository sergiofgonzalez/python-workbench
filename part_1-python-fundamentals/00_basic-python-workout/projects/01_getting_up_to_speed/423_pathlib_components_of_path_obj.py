"""Illustrate the basic components of a pathlib.Path object."""

from pathlib import Path


def main() -> None:
    """Application entry point."""
    path = Path() / "bin" / "utils" / "disktools"
    print(f"{path=}")

    assert path.parts == ("bin", "utils", "disktools")
    assert path.name == "disktools"
    assert path.parent == Path() / "bin" / "utils"
    assert path.suffix == ""  # No suffix since 'disktools' has no extension

    # Now we print them
    print(f"{path.parts=}")
    print(f"{path.name=}")
    print(f"{path.parent=}")
    print(f"{path.suffix=}")

    # Another example with a suffix
    path_with_suffix = Path() / "to" / "img.png"

    assert path_with_suffix.parts == ("to", "img.png")
    assert path_with_suffix.name == "img.png"
    assert path_with_suffix.parent == Path() / "to"
    assert path_with_suffix.suffix == ".png"

    # Now we print them
    print("=" * 40)
    print(f"{path_with_suffix.parts=}")
    print(f"{path_with_suffix.name=}")
    print(f"{path_with_suffix.parent=}")
    print(f"{path_with_suffix.suffix=}")


if __name__ == "__main__":
    main()
