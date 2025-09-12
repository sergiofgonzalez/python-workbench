"""Illustrate the basics of receiving command-line arguments."""

import sys


def main() -> None:
    """Application entry point."""
    print("Number of arguments received:", len(sys.argv) - 1)
    print("Arguments received:", sys.argv[1:])
    for i, arg in enumerate(sys.argv[1:], start=1):
        print(f"Argument {i}: {arg}")
    # extra arg that is always there
    print(f"Program name: {sys.argv[0]=}")

if __name__ == "__main__":
    main()
