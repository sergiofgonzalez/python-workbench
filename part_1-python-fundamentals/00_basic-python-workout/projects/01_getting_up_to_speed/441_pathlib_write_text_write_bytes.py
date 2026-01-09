"""Using pathlib to write text and bytes to files."""

from pathlib import Path

base_path = Path("data", "out_data", "tmp")


def main() -> None:
    """Application entry point."""
    # using write text to write to a file without explicitly opening it
    text_file = base_path / "sample_text.txt"
    text_content = "Hello, World!\nThis is a sample text file.\n"
    text_file.write_text(text_content, encoding="utf-8")
    print(f"Wrote text to {text_file}")

    # using write_text doesn't append, it overwrites
    additional_text = "Adding another line.\n"
    text_file.write_text(additional_text, encoding="utf-8")
    print(f"Overwrote text in {text_file}")

    # printing the contents
    read_back_text = text_file.read_text(encoding="utf-8")
    print(f"Contents of {text_file}:\n{read_back_text}")
    print("=" * 40)

    # using write_bytes to write binary data to a file
    binary_file = base_path / "sample_binary.bin"
    binary_content = str.encode(
        "This is some text that will be transformed to bytes.\r\n",
    )
    binary_file.write_bytes(binary_content)
    print(f"Wrote bytes to {binary_file}")

    # printing the binary contents
    read_back_bytes = binary_file.read_bytes()
    print(f"Contents of {binary_file} (as bytes):\n{read_back_bytes}")


if __name__ == "__main__":
    main()
