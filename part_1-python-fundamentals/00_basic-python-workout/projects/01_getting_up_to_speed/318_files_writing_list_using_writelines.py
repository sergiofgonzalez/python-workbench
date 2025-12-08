"""Illustrate how to write a list of strings to a file using writelines()."""

from pathlib import Path

tasks_file_path = Path("data/out_data/tmp/tasks.csv")


def main() -> None:
    """Application entry point."""
    lines = [
        "1001,Homework,5",
        "1002,Laundry,3",
        "1003,Grocery,4",
    ]

    # by default writelines does not add newline characters
    with tasks_file_path.open(mode="w") as file:
        file.writelines(lines)
        print(f"Wrote {len(lines)} lines to {tasks_file_path}")

    print("Reading")
    with tasks_file_path.open() as file:
        text = file.read()
        print(text)
    print("=" * 40)

    # Adding newline characters while writing
    with tasks_file_path.open(mode="w") as file:
        file.writelines(line + "\n" for line in lines)
        print(f"Wrote {len(lines)} lines to {tasks_file_path}")

    with tasks_file_path.open() as file:
        text = file.read()
        print(text)


if __name__ == "__main__":
    main()
