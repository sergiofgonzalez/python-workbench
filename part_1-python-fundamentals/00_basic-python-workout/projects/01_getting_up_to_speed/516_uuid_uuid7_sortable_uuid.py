"""UUID: Hello, UUID7 (sortable UUID)."""

import uuid


def main() -> None:
    """Application entry point."""
    id_v4 = uuid.uuid4()
    id1_v7 = uuid.uuid7()

    print(f"UUID4: {id_v4}")
    print(f"UUID7(1): {id1_v7}")
    print(f"UUID7(1) timestamp: {id1_v7.time}")

    id2_v7 = uuid.uuid7()
    print(f"UUID7(2): {id2_v7}")
    print(f"UUID7(2) timestamp: {id2_v7.time}")

    # Note that they're correctly ordered by their timestamp, even if their
    # times are the same
    if id1_v7 < id2_v7:
        print("UUID7(1) is less than UUID7(2)")
    elif id1_v7 > id2_v7:
        print("UUID7(1) is greater than UUID7(2)")
    else:
        print("UUID7(1) is equal to UUID7(2)")

    # You can convert UUID7 to a string using str()
    str_id1_v7 = str(id1_v7)
    print(f"UUID7(1) as string: {str_id1_v7} (len: {len(str_id1_v7)})")

    # You can parse it back to a UUID object, and it retains the timestamp information
    parsed_id1_v7 = uuid.UUID(str_id1_v7)
    print(f"Parsed UUID7(1): {parsed_id1_v7}")
    print(f"Parsed UUID7(1) timestamp: {parsed_id1_v7.time}")

    # You can also get the hexadecimal representation of the UUID7, which is a
    # 32-character string without dashes
    hex_id1_v7 = id1_v7.hex
    print(
        f"UUID7(1) as hex: {hex_id1_v7} (type: {type(hex_id1_v7)}, "
        f"len: {len(hex_id1_v7)})",
    )


if __name__ == "__main__":
    main()
