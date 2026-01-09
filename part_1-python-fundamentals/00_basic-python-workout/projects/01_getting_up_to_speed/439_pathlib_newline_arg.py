"""Exploring the newline argument in file handling."""

from pathlib import Path

base_path = Path("data", "in_data", "439_pathlib_newline_arg")


def create_old_mac_file(file_path: Path) -> None:
    r"""Create a file with old Mac-style line endings (\r).

    Args:
        file_path (Path): The path to the file to create.

    """
    lines = ["First line\r", "Second line\r", "Third line\r"]
    with file_path.open("w", newline="") as file:
        file.writelines(lines)


def main() -> None:  # noqa: C901
    """Application entry point."""
    # in case you're wondering how to create a file with old Mac-style line endings
    # old_mac_file = base_path / "old_mac_file.txt"  # noqa: ERA001
    # create_old_mac_file(old_mac_file)  # noqa: ERA001
    # print(f"Created file with old Mac-style line endings at: {old_mac_file}")  # noqa: E501, ERA001

    # Opening the old Mac-style file, default newline handling
    print("================== Old Mac-style File (\\r) ================")
    old_mac_file = base_path / "old_mac_file.txt"
    with old_mac_file.open("r") as file:
        for line in file:
            print(f"Default read line: {line!r}")
    print("=" * 40)

    # Opening the old Mac-style file, specifying newline='\r'
    with old_mac_file.open("r", newline="\r") as file:
        for line in file:
            print(f"Custom newline as '\\r' read line: {line!r}")
    print("=" * 40)

    # Opening the old Mac-style file, specifying newline=''
    with old_mac_file.open("r", newline="") as file:
        for line in file:
            print(f"Custom newline as '' read line: {line!r}")
    print("=" * 40)

    # Opening the old Mac-style file, specifying newline='\n'
    with old_mac_file.open("r", newline="\n") as file:
        for line in file:
            print(f"Custom newline as '\\n' read line: {line!r}")
    print("=" * 40)

    print("================== Windows-style File (\\r\\n) ================")
    # Opening the Windows-style file, default newline handling
    windows_file = base_path / "win_file.txt"
    with windows_file.open("r") as file:
        for line in file:
            print(f"Default read line: {line!r}")
    print("=" * 40)

    # Opening the Windows-style file, specifying newline='\r\n'
    with windows_file.open("r", newline="\r\n") as file:
        for line in file:
            print(f"Custom newline as '\\r\\n' read line: {line!r}")
    print("=" * 40)

    # Opening the Windows-style file, specifying newline=''
    with windows_file.open("r", newline="") as file:
        for line in file:
            print(f"Custom newline as '' read line: {line!r}")
    print("=" * 40)

    # Opening the Windows-style file, specifying newline='\n'
    with windows_file.open("r", newline="\n") as file:
        for line in file:
            print(f"Custom newline as '\\n' read line: {line!r}")
    print("=" * 40)

    # Opening the Unix-style file, default newline handling
    print("================== Unix-style File (\\n) ================")
    unix_file = base_path / "linux_file.txt"
    with unix_file.open("r") as file:
        for line in file:
            print(f"Default read line: {line!r}")
    print("=" * 40)

    # Opening the Unix-style file, specifying newline='\n'
    with unix_file.open("r", newline="\n") as file:
        for line in file:
            print(f"Custom newline as '\\n' read line: {line!r}")
    print("=" * 40)

    # Opening the Unix-style file, specifying newline=''
    with unix_file.open("r", newline="") as file:
        for line in file:
            print(f"Custom newline as '' read line: {line!r}")
    print("=" * 40)

    # Opening the Unix-style file, specifying newline='\r'
    with unix_file.open("r", newline="\r") as file:
        for line in file:
            print(f"Custom newline as '\\r' read line: {line!r}")
    print("=" * 40)


if __name__ == "__main__":
    main()
