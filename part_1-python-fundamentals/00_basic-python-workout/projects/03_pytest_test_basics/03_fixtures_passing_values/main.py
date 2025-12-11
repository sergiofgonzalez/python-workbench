"""Simple application making use of the utils/mathutils module."""

from utils.mathutils import add


def main() -> None:
    """Application entry point."""
    input_a = input("Enter the first number: ")
    input_b = input("Enter the second number: ")

    try:
        a = float(input_a)
        b = float(input_b)
        print(f"{a} + {b} = {add(a, b)}")
    except ValueError:
        print("Invalid input. Please enter numeric values.")


if __name__ == "__main__":
    main()
