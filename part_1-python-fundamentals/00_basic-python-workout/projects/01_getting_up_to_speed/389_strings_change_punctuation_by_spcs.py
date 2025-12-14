"""Illustrates how to change punctuation in a string to spaces."""


def main() -> None:
    """Application entry point."""
    s = "Hello, world!"
    s_chars = list(s)
    result_chars = []
    for i in range(4, -1, -1):
        result_chars.append(s_chars[i])  # noqa: PERF401
    modified_s = "".join(result_chars)
    print(f"Original string: {s}")
    print(f"Modified string: {modified_s}")


if __name__ == "__main__":
    main()
