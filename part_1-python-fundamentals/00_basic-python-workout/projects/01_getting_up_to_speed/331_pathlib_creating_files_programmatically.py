"""Illustrates creating files programmatically with pathlib."""

from pathlib import Path


def main() -> None:
    """Application entry point."""
    base_name = "subject_"
    nums = range(123, 126)
    extensions = [".config", ".dat", ".txt"]

    base_path = Path("data/out_data/tmp/my_files")
    base_path.mkdir(parents=True, exist_ok=True)

    for num in nums:
        for ext in extensions:
            file_path = base_path / f"{base_name}{num}{ext}"
            file_path.touch()
            print(f"Creating file: {file_path.resolve()}")


if __name__ == "__main__":
    main()
