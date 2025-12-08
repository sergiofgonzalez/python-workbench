"""Illustrate how to read a single line from a file using readline()."""

from pathlib import Path

tasks_file_path = Path("data/in_data/tasks/tasks.csv")


def main() -> None:
    """Application entry point."""
    with tasks_file_path.open() as file:
        # Read the first line from the file
        first_line = file.readline()
        print(f"First line: {first_line.rstrip()!r}")

        # Read the second line from the file
        second_line = file.readline()
        print(f"Second line: {second_line.rstrip()!r}")

        # Read the first 5 characters from the third line
        third_line_partial = file.readline(5)
        print(f"First 5 characters of third line: {third_line_partial!r}")

        # Read the next 8 characters from the third line
        third_line_partial_continued = file.readline(8)
        print(f"Next 8 characters of third line: {third_line_partial_continued!r}")

        # Read the rest of the third line
        third_line_rest = file.readline()
        print(f"Rest of third line: {third_line_rest.rstrip()!r}")

if __name__ == "__main__":
    main()
