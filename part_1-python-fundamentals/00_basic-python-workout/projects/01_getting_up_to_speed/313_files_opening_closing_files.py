"""Opening and closing files with Path.open and the context manager (recommended)."""

from pathlib import Path


def main() -> None:
    """Application entry point."""
    # By default, files are opened in read mode ('r')
    file_path = Path("data/in_data/tasks/tasks.csv")
    with file_path.open() as file:
        text = file.read()
        print(text)
        print("---")
        print(f"{text!r}")
    print("=" * 40)

    # Handling exceptions while ensuring the file is closed
    try:
        with file_path.open() as file:
            text = file.read()
            print(text)
    except Exception as e:  # noqa: BLE001
        print(f"An error occurred: {e} (type: {type(e).__name__})")

if __name__ == "__main__":
    main()
