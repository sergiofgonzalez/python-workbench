"""Illustrates what happens when you schedule a coroutine without awaiting it."""

import asyncio
from pathlib import Path

base_path = Path("data", "out_data", "tmp")


async def create_file_async(name: str) -> None:
    """Create a file with the given name after a short delay."""
    file_path = base_path / name
    with file_path.open("w") as file:
        # Uncomment to see it fail
        # if name == "file2.txt":
        #     await asyncio.sleep(2)  # noqa: ERA001
        file.write(f"{name}: This file was created asynchronously.\n")
    print(f"Created file: {name}")


async def main() -> None:
    """Application entry point."""
        # this will fail right away if no await

    try:
        create_file_async("file4.txt")
        asyncio.gather(
            create_file_async("file1.txt"),
            create_file_async("file2.txt"),
            create_file_async("file3.txt"),
        )
    # this won't actually catch anything, but shows that no await means no
    # exception handling
    except RuntimeError as ex:
        print(f"Caught an exception: {ex}")




if __name__ == "__main__":
    asyncio.run(main())
    print("== done")
