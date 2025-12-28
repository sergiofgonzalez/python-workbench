"""Illustrates how to use the `pathlib.glob` method to find files matching a pattern."""

from pathlib import Path


def main() -> None:
    """Application entry point."""
    cur_dir = Path()  # Current directory
    pattern = "1?[2,4,6]*.py"  # Pattern to match
    for file_path in cur_dir.glob(pattern):
        print(file_path.name)
    print("=" * 40)

    # listing all image files in a directory
    img_dir = Path("data") / "out_data" / "tmp"
    # match all .png, .jpg, .jpeg, and gif files
    img_pattern = "*.{png,jpg,jpeg,gif}"
    for img_file in img_dir.glob(img_pattern):
        print(img_file.name)
    print("=" * 40)


if __name__ == "__main__":
    main()
