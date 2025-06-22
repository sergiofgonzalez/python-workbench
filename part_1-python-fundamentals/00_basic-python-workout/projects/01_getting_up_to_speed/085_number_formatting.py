"""Illustrate basic number formatting in Python."""


def main() -> None:
    """Application entry point."""
    # Print a decimal number with commas as thousands separators
    num = 1000000007
    print(f"{num:,d}")
    print(f"{num:,}")

    # Print a floating point with two and four decimal places
    num = 1.23456
    print(f"{num:.2f}")
    print(f"{num:.4f}")

    # Print a floating point using scientific notation
    num = 0.00000000412733
    print(f"{num:e}")
    print(f"{num:.2e}")  # with two decimal places

    # Print a floating point with general formatting
    # this will use the shortest representation between fixed-point and sci notation
    num = 0.00000000412733
    print(f"{num:g}")
    print(f"{num:.2g}")  # with two significant digits
    num = 123.45
    print(f"{num:g}")

    # Print as a percentage
    num = 0.179323
    print(f"{num:%}")
    print(f"{num:.2%}")  # with two decimal places

    # Print hex value
    num = 255
    print(f"{num:#x}")  # with '0x' prefix
    print(f"{num:x}")  # without '0x' prefix
    print(f"{num:#X}")  # with '0X' prefix
    print(f"{num:X}")  # without '0X' prefix, chars in uppercase

    # Print binary value
    num = 255
    print(f"{num:#b}")  # with '0b' prefix
    print(f"{num:b}")  # without '0b' prefix


if __name__ == "__main__":
    main()
