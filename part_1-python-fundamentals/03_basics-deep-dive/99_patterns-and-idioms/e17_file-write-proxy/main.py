"""Main application."""

from pathlib import Path

from write_proxy import WriteProxy


def main() -> None:
    """Application entry point."""
    dst_filename = Path("outfiles") / "out.txt"
    with dst_filename.open("w") as f:
        f.write("This is a line in a file.\n")
        f.write("There are many lines like this one.\n")
        f.write("But this is mine.\n")

    dst_filename = Path("outfiles") / "out_2.txt"
    with dst_filename.open("w") as f:
        f_proxy = WriteProxy(f)
        f_proxy.write("This is a line in a file.\n")
        f_proxy.write("There are many lines like this one.\n")
        f_proxy.write("But this is mine.\n")
        f.write(
            "This line will not show in the terminal, but will be written on file.\n"
        )


if __name__ == "__main__":
    main()
