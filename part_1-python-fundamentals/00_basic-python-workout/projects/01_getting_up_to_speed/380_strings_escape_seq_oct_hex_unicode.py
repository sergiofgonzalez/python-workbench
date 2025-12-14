"""Illustrates the escape sequences for octal, hex, and Unicode."""


def main() -> None:
    """Application entry point."""
    octal_escape = "\101\102\103"  # Octal for 'A', 'B', 'C'
    hex_escape = "\x41\x42\x43"  # Hex for 'A', 'B', 'C'
    unicode_escape = "\u0041\u0042\u0043"  # Unicode for 'A', 'B', 'C'
    unicode_escape_long = (
        "\U00000041\U00000042\U00000043"  # Long Unicode for 'A', 'B', 'C'
    )
    unicode_human_readable_labels = (
        "\N{LATIN CAPITAL LETTER A}\N{LATIN CAPITAL LETTER B}\N{LATIN CAPITAL LETTER C}"
    )

    print("Octal Escape Sequence:", octal_escape)
    print("Hex Escape Sequence:", hex_escape)
    print("Unicode Escape Sequence:", unicode_escape)
    print("Long Unicode Escape Sequence:", unicode_escape_long)
    print("Unicode with Human-Readable Labels:", unicode_human_readable_labels)


if __name__ == "__main__":
    main()
