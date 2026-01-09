"""Illustrates how to read from redirected stdin and write to redirected stdout."""

import sys
from pathlib import Path

in_base_path = Path("data", "in_data", "443_redirecting_stdin_stdout")
out_base_path = Path("data", "out_data", "tmp")


def main() -> None:
    """Application entry point."""
    user_input_file = in_base_path / "user_input_in_file.txt"

    with user_input_file.open("r") as file:
        sys.stdin = file
        print("Reading input from redirected sys.stdin:")
        name = sys.stdin.readline().strip()
        age = sys.stdin.readline().strip()
        print(f"Name: {name!r}")
        print(f"Age: {age!r}")

        # Look, ma, it wors with input() as well!
        fave_actor = input().strip()

    # Redirecting sys.stdout to a file
    output_file = out_base_path / "output_from_stdout.txt"
    with output_file.open("w") as file:
        sys.stdout = file
        print(f"User Name: {name}")
        print(f"User Age: {age}")
        print(f"Favorite Actor: {fave_actor}")

    # Reset sys.stdout, sys.stdin to default
    sys.stdout = sys.__stdout__
    sys.stdin = sys.__stdin__
    print(f"Output written to: {output_file}")


if __name__ == "__main__":
    main()
