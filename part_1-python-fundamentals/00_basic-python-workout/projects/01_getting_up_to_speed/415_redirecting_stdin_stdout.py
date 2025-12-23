"""Illustrates how to redirect stdin and stdout in Python."""

import sys


def main() -> None:
    """Application entry point."""
    stdin_content = sys.stdin.read()
    sys.stdout.write(f"{stdin_content.upper()=}\n")


if __name__ == "__main__":
    main()
