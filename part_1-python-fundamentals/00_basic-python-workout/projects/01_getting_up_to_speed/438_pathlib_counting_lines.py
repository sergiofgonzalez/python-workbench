"""Illustrates how to count lines in a file using pathlib."""

from pathlib import Path

base_path = Path("data", "in_data", "438_pathlib_counting_lines")


def count_lines_in_file(file_path: Path) -> int:
    """Count the number of lines in a file.

    Args:
        file_path (Path): The path to the file.

    Returns:
        int: The number of lines in the file.

    """
    count = 0
    with file_path.open("r", encoding="utf-8") as file:
        while file.readline():
            count += 1
    return count


def main() -> None:
    """Application entry point."""
    file_no_final_newline = base_path / "file_1.txt"

    lines_count_1 = count_lines_in_file(file_no_final_newline)
    print(f"Number of lines in '{file_no_final_newline.name}': {lines_count_1}")

    file_final_newline = base_path / "file_2.txt"
    lines_count_2 = count_lines_in_file(file_final_newline)
    print(f"Number of lines in '{file_final_newline.name}': {lines_count_2}")


if __name__ == "__main__":
    main()
