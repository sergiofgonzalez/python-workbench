"""Concatenating file contents asynchronously."""

import asyncio
import time

import aiofiles

MIN_REQUIRED_NUM_ARGUMENTS = 3


async def concat_files(*args: str) -> None:
    """Concatenate the files given, where the last argument is the output file."""
    if len(args) < MIN_REQUIRED_NUM_ARGUMENTS:
        msg = "At least two input files and an output file are required"
        raise ValueError(msg)

    input_files = args[0:-1]
    dest_file = args[-1]

    accumulated_content = ""
    for input_file in input_files:
        async with aiofiles.open(input_file) as f:
            print(f"open {input_file}: done")
            file_content = await f.read()
            print(f"read {input_file}: done")
        accumulated_content += file_content

    async with aiofiles.open(dest_file, mode="w") as f:
        print(f"open {dest_file}: done")
        await f.write(accumulated_content)
        print(f"write {dest_file}: done")


async def main() -> None:
    """Async application entry point."""
    start = time.perf_counter()
    try:
        await concat_files(
            "sample_files/foo.txt",
            "sample_files/bar.txt",
            "sample_files/foobar.txt",
            "sample_files/out.txt",
        )
        print(f"Process took {time.perf_counter() - start:.3f} seconds")
    except OSError as e:
        print(f"ERROR: could not concatenate files: {e} ({type(e)})")


if __name__ == "__main__":
    asyncio.run(main())
