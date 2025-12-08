"""Opening and closing files without the context manager (discouraged)."""


def main() -> None:
    """Application entry point."""
    # By default, files are opened in read mode ('r')
    file = open("data/in_data/tasks/tasks.csv")  # noqa: PTH123, SIM115
    text = file.read()
    print(text)
    print("---")
    print(f"{text!r}")
    file.close()
    print("=" * 40)
    # Better to use try-finally to ensure the file is closed
    file = open("data/in_data/tasks/tasks.csv")  # noqa: PTH123, SIM115
    try:
        text = file.read()
        print(text)
    except Exception as e:  # noqa: BLE001
        print(f"An error occurred: {e} (type: {type(e).__name__})")
    finally:
        file.close()


if __name__ == "__main__":
    main()
