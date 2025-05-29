"""Illustrate use of bit_length and id."""


def main() -> None:
    """Application entry point."""
    num_int = 42
    num_float = 42.0

    print(
        f"num_int: {num_int}, "
        f"address: {id(num_int)}, bit length: {num_int.bit_length()}"
    )
    print(
        f"num_float: {num_float}, "
        f"address: {id(num_float)}, "
        f"bit length: {num_float.bit_length() if hasattr(num_float, 'bit_length') else 'N/A'}" # noqa: COM812, E501
    )

if __name__ == "__main__":
    main()
