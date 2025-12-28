"""Illustrate fileinput with custom files."""

import fileinput


def main() -> None:
    """Application entry point."""
    file1 = "data/in_data/419_fileinput_hello/infile_1.txt"
    file2 = "data/in_data/419_fileinput_hello/infile_2.txt"

    for line in fileinput.input(files=(file1, file2)):  # noqa: SIM115
        print(
            f"{fileinput.filename()} | {fileinput.filelineno()} |"
            f" {fileinput.lineno()} | {line}",
            end="",
        )  # line already has newline


if __name__ == "__main__":
    main()
