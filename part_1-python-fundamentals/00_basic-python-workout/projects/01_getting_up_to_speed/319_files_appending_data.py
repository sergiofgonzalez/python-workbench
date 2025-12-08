"""Illustrates how to append data to a file."""

from pathlib import Path

in_tasks_file_path = Path("data/in_data/tasks/tasks.csv")
out_tasks_file_path = Path("data/out_data/tmp/tasks.csv")


def main() -> None:
    """Application entry point."""
    with in_tasks_file_path.open() as in_file:
        data = in_file.read()
    with out_tasks_file_path.open(mode="w") as out_file:
        out_file.write(data)
        print(f"Wrote data to {out_tasks_file_path}")

    with out_tasks_file_path.open() as file:
        text = file.read()
        print(text)
    print("== appending ==")
    # newline management might be tricky when appending between Linux and Windows
    with out_tasks_file_path.open(mode="a") as out_file:
        out_file.write("1004,Museum,3\n")
        print(f"Appended data to {out_tasks_file_path}")
    with out_tasks_file_path.open() as file:
        text = file.read()
        print(text)
if __name__ == "__main__":
    main()
