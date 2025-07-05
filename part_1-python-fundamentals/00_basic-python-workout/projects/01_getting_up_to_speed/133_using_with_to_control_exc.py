"""Illustrate how to use with to control file exceptions."""

from pathlib import Path

out_path = Path.cwd() / "data" / "out_data" / "133_using_with_to_control_exc"


def main() -> None:
    """Application entry point."""
    # Writing a file with no exception handling
    # If there is an error, the file may not be closed properly
    file_path = out_path / "001_no_exception_handling.txt"
    file_obj = file_path.open("w")
    file_obj.write("This is a test file with no exception handling.\n")
    file_obj.close()

    # Writing a file with exception handling using try-except
    # The error will be handled properly, but the code is ugly as hell
    try:
        file_path = out_path / "002_with_exception_handling.txt"
        file_obj = file_path.open("w")
        file_obj.write(
            "This is a test file with exception handling using try-except.\n",
        )
    except OSError as e:
        print(f"An error occurred: {e}")
    finally:
        file_obj.close()

    # Writing a file with exception handling using with
    # Any error will be handled properly and the code is clean and readable
    file_path = out_path / "003_with_exception_handling_using_with.txt"
    with file_path.open("w") as file_obj:
        file_obj.write(
            "This is a test file with exception handling using with.\n",
        )


if __name__ == "__main__":
    main()
