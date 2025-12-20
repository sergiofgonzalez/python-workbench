"""Illustrates a couple of ways of breaking up long lines in Python."""


def main() -> None:
    """Application entry point."""
    x = 100 + 200 + 300 + 400 + 500 + 600 + 700 + 800 + 900 \
        + 1000 + 1100 + 1200 + 1300 + 1400 + 1500
    print(x)

    s = "a very large string that most probably will reach the threshold that I \
        have established"
    print(f"{s!r}")

    # Using parentheses to break up long lines is cleaner and clearer
    s = ("a very large string that most probably will reach the threshold that I "
        "have established")
    print(f"{s!r}")


if __name__ == "__main__":
    main()
