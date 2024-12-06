"""Illustrate the monkey patching technique in Python."""

from pathlib import Path

from mockread import disable_mock, enable_mock


def main() -> None:
    """App entry point."""
    with Path("./README.md").open("r") as f:
        lines = f.read()
        print(lines)

    print("=" * 80)
    enable_mock("Hello to Jason Isaacs!")
    with Path("./fake-path.md").open("r") as f:
        lines = f.read()
        print(lines)

    print("=" * 80)
    disable_mock()
    with Path("./README.md").open("r") as f:
        lines = f.read()
        print(lines)


if __name__ == "__main__":
    main()
