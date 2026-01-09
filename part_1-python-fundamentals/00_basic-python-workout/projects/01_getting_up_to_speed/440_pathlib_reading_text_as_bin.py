"""Illustrates how to read a file in binary mode using pathlib."""

from pathlib import Path

base_path = Path("data", "in_data", "439_pathlib_newline_arg")


def main() -> None:
    """Application entry point."""
    old_mac_file = base_path / "old_mac_file.txt"
    with old_mac_file.open("rb") as bin_file:
        chunk_1 = bin_file.read(4)
        chunk_2 = bin_file.read()
        if bin_file.read() == b"":
            print("Reached end of file after reading two chunks.")
    print(f"First chunk (4 bytes): {chunk_1!r}")
    print(f"Second chunk (rest of file): {chunk_2!r}")


if __name__ == "__main__":
    main()
