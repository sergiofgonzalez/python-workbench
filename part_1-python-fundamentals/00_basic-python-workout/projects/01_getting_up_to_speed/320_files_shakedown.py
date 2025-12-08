"""Illustrates file operations shakedown."""

from pathlib import Path

in_tasks_file_path = Path("data/in_data/tasks/tasks.csv")
out_tasks_file_path = Path("data/out_data/tmp/tasks.csv")


def print_file_contents(in_file: Path) -> None:
    """Print file contents."""
    with in_file.open() as f:
        contents = f.read()
    print(f"{contents=!r}")


def main() -> None:  # noqa: PLR0912, PLR0915
    """Application entry point."""
    # Reading from file

    # read(): reads the whole file as a single string
    print("== Reading with read() ==")
    with in_tasks_file_path.open() as in_file:
        data = in_file.read()
        print(f"{data!r}")
    print("=" * 60)

    # readline(): reads a single line from the file
    print("== Reading with readline() ==")
    with in_tasks_file_path.open() as in_file:
        while data:
            data = in_file.readline()
            if data:
                print(f"{data!r}")
            else:
                print("EOF (no data to print)")
    print("=" * 60)

    # for: reading from the file with a for loop

    print("== Reading with for loop ==")
    with in_tasks_file_path.open() as in_file:
        for line in in_file:
            print(f"{line!r}")
    print("=" * 60)

    # readlines(): reads all lines into a list of strings
    print("=== Reading with readlines() ===")
    with in_tasks_file_path.open() as in_file:
        lines = in_file.readlines()
        print(lines)
    print("=" * 60)

    # read(), readline(), readlines() allow for a size argument
    print("=== read() with size (reading 5 chars each time) ===")
    with in_tasks_file_path.open() as in_file:
        data = in_file.read(5)
        while data:
            if data:
                print(f"{data!r}")
                data = in_file.read(5)
            else:
                print("EOF (no data to print)")
    print("=" * 60)
    with in_tasks_file_path.open() as in_file:
        data = in_file.readline(5)
        while data:
            if data:
                print(f"{data!r}")
                data = in_file.readline(5)
            else:
                print("EOF (no data to print)")
    print("=" * 60)
    with in_tasks_file_path.open() as in_file:
        data = in_file.readlines(5)
        while data:
            if data:
                print(f"{data!r}")
                data = in_file.readlines(5)
            else:
                print("EOF (no data to print)")
    print("=" * 60)

    # Writing to file

    # write(): write the str to file
    print("=== Writing with write() ===")
    with out_tasks_file_path.open("w") as out_file:
        out_file.write("1001,Homework,5")
    print_file_contents(out_tasks_file_path)
    print("=" * 60)

    # writelines(): write list of strings to file
    print("=== Writing with writelines() ===")
    lines = [
        "1001,Homework,5",
        "1002,Laundry,3",
    ]
    with out_tasks_file_path.open("w") as out_file:
        out_file.writelines(lines)
    print_file_contents(out_tasks_file_path)
    print("=" * 60)

    # File modes: illustrating where the cursor is positioned when opening

    # mode="r": read mode, cursor placed at the start of the file
    print("=== mode=r ===")
    with in_tasks_file_path.open() as in_file:
        data = in_file.read()
    print_file_contents(in_tasks_file_path)
    print("=" * 60)

    # mode="w": write mode, cursor placed at the start of the file
    # this mode truncates existing contents and creates file if it doesn't exist
    print("=== mode=w ===")
    new_out_tasks_file_path = Path("data/out_data/tmp/tasks2.csv")
    with new_out_tasks_file_path.open("w") as out_file:
        out_file.write("1003,Cleaning,2")
    print_file_contents(new_out_tasks_file_path)
    print("=" * 60)

    with out_tasks_file_path.open("w") as out_file:
        out_file.write("1003,Cleaning,2")
    print_file_contents(out_tasks_file_path)
    print("=" * 60)

    # mode="a": append mode, cursor placed at the end of the file
    # this mode appends or creates file if it doesn't exist
    print("=== mode=a ===")
    new_out_tasks_file_path = Path("data/out_data/tmp/tasks3.csv")
    with new_out_tasks_file_path.open("a") as out_file:
        out_file.write("1004,Gym,1")
    print_file_contents(new_out_tasks_file_path)
    print("=" * 60)

    with out_tasks_file_path.open("a") as out_file:
        out_file.write("1004,Gym,1")
    print_file_contents(out_tasks_file_path)
    print("=" * 60)

    # mode="r+": read/write mode, cursor placed at the beginning of the file
    # the file must exist and it is opened for both reading and writing
    print("=== mode=r+ ===")
    with out_tasks_file_path.open("r+") as out_file:
        out_file.readline()
        out_file.write("1004,Gym,1\n")
    print_file_contents(out_tasks_file_path)
    print("=" * 60)

    # mode="w+": read/write mode, cursor placed at the beginning of the file
    # the file might or might not exist and it's opened for both reading and writing
    # if the file exists, it is truncated
    print("=== mode=w+ ===")
    with out_tasks_file_path.open("w+") as out_file:
        out_file.readline()
        out_file.write("1005,Reading,4\n")
    print_file_contents(out_tasks_file_path)
    print("=" * 60)

    # mode="a+": read/write mode, cursor placed at the end of the file
    # the file might or might not exist and it's opened for both reading and writing
    print("=== mode=a+ ===")
    with out_tasks_file_path.open("a+") as out_file:
        out_file.readline()
        out_file.write("1006,Videogames,8\n")
    print_file_contents(out_tasks_file_path)
    print("=" * 60)

    # mode="x": write mode, cursor placed at the beginning of the file
    # this mode creates the file, but fails if the file already exists
    print("=== mode=x ===")
    new_out_tasks_file_path = Path("data/out_data/tmp/tasks4.csv")
    with new_out_tasks_file_path.open("x") as out_file:
        out_file.write("1007,Shopping,6")
    print_file_contents(new_out_tasks_file_path)
    print("=" * 60)


if __name__ == "__main__":
    main()
