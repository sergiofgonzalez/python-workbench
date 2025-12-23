"""fileinput basic example to read lines from files specified as command line args."""

import fileinput


def main() -> None:
    """Application entry point."""
    # Basic usage: read lines from the files specified as command line arguments
    # for line in fileinput.input():
    #     print(f"{line=}")  # noqa: ERA001
    # print("=" * 40)  # noqa: ERA001

    # Exercise
    for line in fileinput.input():  # noqa: SIM115
        if fileinput.isfirstline():
            print(f"--- Start of file: {fileinput.filename()} ---")
        if line.startswith("#"):
            continue
        if fileinput.isstdin():
            print(
                f"<stdin> | {fileinput.filelineno()} | {fileinput.lineno()} | {line}",
                end="",  # line already has newline
            )
        else:
            print(
                f"file | {fileinput.filelineno()} | {fileinput.lineno()} | {line}",
                end="",  # line already has newline
            )


if __name__ == "__main__":
    main()
