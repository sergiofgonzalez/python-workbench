"""Illustrate how to write data to a file using write()."""

import textwrap
from pathlib import Path

tasks_file_path = Path("data/out_data/tmp/tasks.csv")


def main() -> None:
    """Application entry point."""
    contents = textwrap.dedent("""\
        1001,Homework,5
        1002,Laundry,3
        1003,Grocery Shopping,4\
        """)
    with tasks_file_path.open(mode="w") as file:
        bytes_written = file.write(contents)
        print(f"Wrote {bytes_written} bytes to {tasks_file_path}")

    with tasks_file_path.open() as file:
        text = file.read()
        print(text)


if __name__ == "__main__":
    main()
