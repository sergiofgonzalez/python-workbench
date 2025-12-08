"""Creating a directory with pathlib."""

from pathlib import Path

tmp_dir = Path("data/out_data/tmp")


def main() -> None:
    """Application entry point."""
    new_dir = tmp_dir / "my_dir"
    new_dir.mkdir(parents=True, exist_ok=True)
    print(f"Directory created at: {new_dir.resolve()}")

    assert new_dir.exists()
    assert new_dir.is_dir()
    print("=== Directory creation verified ===")


if __name__ == "__main__":
    main()
