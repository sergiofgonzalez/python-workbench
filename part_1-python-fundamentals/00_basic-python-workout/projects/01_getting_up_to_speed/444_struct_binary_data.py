"""Illustrates the basics of the struct module."""

import math
import struct
from pathlib import Path

base_path = Path("data", "out_data", "tmp")


def main() -> None:
    """Application entry point."""
    format_string = "hd7s"
    rec1 = struct.pack(format_string, 42, math.pi, b"goodbye")
    rec2 = struct.pack(format_string, 55, math.e, b"hello")
    print(f"Record 1 packed bytes: {rec1!r}")
    print(f"Record 2 packed bytes: {rec2!r}")

    # Now we open a binary file and write the packed records
    binary_file = base_path / "struct_binary_data.bin"
    with binary_file.open("wb") as bin_file:
        bin_file.write(rec1)
        bin_file.write(rec2)
    print(f"Wrote packed records to {binary_file}")

    # Now let's read back the binary data and unpack it
    records = []
    with binary_file.open("rb") as bin_file:
        record_size = struct.calcsize(format_string)
        print(f"Each record is {record_size} bytes long.")
        rec1_read_back_bytes = bin_file.read(record_size)
        rec2_read_back_bytes = bin_file.read(record_size)
        records.append(struct.unpack(format_string, rec1_read_back_bytes))
        records.append(struct.unpack(format_string, rec2_read_back_bytes))

    print("Unpacked records:")
    for i, record in enumerate(records):
        print(f"{i:02d}: {record!r}")


if __name__ == "__main__":
    main()
