"""Illustrates how to build paths using pathlib.Path.joinpath()."""

from pathlib import Path


def main() -> None:
    """Application entry point."""
    result_path = Path().joinpath("bin", "utils", "disktools")
    print(f"{result_path=}")

    assert result_path == Path() / "bin" / "utils" / "disktools"
    assert result_path == Path("bin") / "utils" / "disktools"
    assert result_path == Path("bin/utils/disktools")

    print("== All assertions passed ===")


if __name__ == "__main__":
    main()
