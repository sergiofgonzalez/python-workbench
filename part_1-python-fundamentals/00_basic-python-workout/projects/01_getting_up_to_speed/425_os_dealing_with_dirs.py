"""Illustrates how to deal with directories using the os module."""

import os


def main() -> None:
    """Application entry point."""
    print(f"{os.getcwd()=}")  # Current working directory  # noqa: PTH109
    print(f"{os.curdir=}")  # Current directory symbol
    print(f"{os.pardir=}")  # Parent directory symbol
    print(f"{os.listdir()=}")  # List of entries in current directory  # noqa: PTH208

    # changing directories and listing contents
    os.chdir(os.pardir)  # Change to parent directory
    print(f"After chdir to parent, {os.getcwd()=}")  # Current  # noqa: PTH109
    print(f"{os.listdir()=}")  # List of entries in current directory  # noqa: PTH208

    # build a path to a subdirectory
    os_path = os.path.join("bin", "utils", "disktools")  # noqa: PTH118
    print(f"Built path: {os_path=}")

    # build a path with supaths
    os_path = os.path.join("mydir/bin", "utils", "disktools", "chkdsk")  # noqa: PTH118
    print(f"Built path with subpaths: {os_path=}")

    assert os_path == os.path.join("mydir", "bin", "utils", "disktools", "chkdsk")  # noqa: PTH118

    os.path.join("path", "to", "some", "dir")  # noqa: PTH118
    print(f"{os.path.split(os_path)=}")  # Split into head and tail

    os_path = os.path.join("path", "to", "some", "dir", "img.png")  # noqa: PTH118
    print(f"{os.path.basename(os_path)=}")  # noqa: PTH119
    print(f"{os.path.dirname(os_path)=}")  # noqa: PTH120

    os_path = os.path.join("path", "to", "img.png")  # noqa: PTH118
    print(f"{os.path.splitext(os_path)=}")  # Split into root and ext  # noqa: PTH122

    os_path = os.path.join("path", "to", "some", "dir")  # noqa: PTH118
    print(f"{os.path.splitext(os_path)=}")  # Split into root and ext  # noqa: PTH122

    os_path = os.path.join("$HOME", "Downloads")  # noqa: PTH118
    print(f"{os.path.expandvars(os_path)=}")

    os_path = os.path.join("~", "Downloads")  # noqa: PTH118
    print(f"{os.path.expanduser(os_path)=}")  # noqa: PTH111

    os_path = os.path.join(os.pardir, "mini-projects")  # noqa: PTH118
    print(f"{os_path=}")
    print(f"{os.path.isabs(os_path)=}")  # Is absolute path?  # noqa: PTH117

    os_paths = ["C:\\Windows\\System32", "C:", "C:\\", "\\Windows\\System32"]
    for os_path in os_paths:
        print(f"{os_path=}")
        print(f"{os.path.isabs(os_path)=}")  # Is absolute path?  # noqa: PTH117


if __name__ == "__main__":
    main()
