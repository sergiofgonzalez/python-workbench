"""Illustrates how to read environment variables."""
import os

def main() -> None:
    """Application entry point."""
    my_name = os.getenv("MY_NAME", "world")
    print(f"Hello, {my_name}!")


if __name__ == "__main__":
    main()
