"""Replacing references to current directory and parent directory using pathlib."""

import os
from pathlib import Path


def get_cleaned_dir_path(original_path: Path) -> str:
    """Replace references to current directory (.) and parent directory (..) in a path.

    Args:
        original_path (str): The original file path.

    Returns:
        str: The cleaned file path with . and .. resolved.

    """
    if original_path in (Path(os.curdir), Path(os.pardir)):
        return f"{original_path.resolve().name}{os.sep}"
    if not str(original_path).endswith(os.sep):
        return f"{original_path}{os.sep}"
    return str(original_path)


def main() -> None:
    """Application entry point."""
    examples = [
        Path("."),  # noqa: PTH201
        Path(".."),
        Path("./folder"),
        Path("../folder"),
        Path("folder"),
        Path("/folder"),
        Path("/folder/subfolder/"),
        Path("folder/"),
    ]

    for example in examples:
        cleaned = get_cleaned_dir_path(example)
        print(f"Original: {example} -> Cleaned: {cleaned}")


if __name__ == "__main__":
    main()
