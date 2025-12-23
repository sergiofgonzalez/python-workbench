"""A practical example with stdin/stdout redirection in an app taking arguments."""

import sys


def main() -> None:
    """Application entry point."""
    if len(sys.argv) != 3:  # noqa: PLR2004
        sys.stderr.write(f"Usage: python {sys.argv[0]} <old_string> <new_string>\n")
        sys.exit(1)

    stdin_content = sys.stdin.read()
    stdin_content = stdin_content.replace(sys.argv[1], sys.argv[2])
    sys.stdout.write(stdin_content)


if __name__ == "__main__":
    main()
