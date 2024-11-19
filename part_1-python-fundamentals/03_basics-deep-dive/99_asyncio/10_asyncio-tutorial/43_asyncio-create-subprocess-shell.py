"""Illustrates how to use asyncio.create_subprocess_shell() to run commands."""

import asyncio


async def main() -> None:
    """Async Main coroutine."""
    # Start executing a command in a separate subprocess
    # Output will be displayed in the command line automatically
    process = await asyncio.create_subprocess_shell("echo Hello, world")
    print(f"subprocess: {process}")

    # Start executing a command in a separate subprocess, piping stdout
    print("=" * 80)
    process = await asyncio.create_subprocess_shell(
        "echo Hello, world",
        stdout=asyncio.subprocess.PIPE,
    )
    # read a line from the process output stream
    line = await process.stdout.readline()
    print(f"{line=}")

    # # Start executing a command in a separate subprocess, piping stdin
    print("=" * 80)
    process = await asyncio.create_subprocess_shell(
        "wc -c",
        stdin=asyncio.subprocess.PIPE,
    )
    # send some data to the process input stream
    await process.communicate(input=b"the quick brown fox")

    # Start executing a command in a separate subprocess, piping stdin and
    # communicate using streamwriter methods
    print("=" * 80)
    process = await asyncio.create_subprocess_shell(
        "wc -c",
        stdin=asyncio.subprocess.PIPE,
    )
    # send some data to the process input stream using the StreamWriter
    process.stdin.write(b"the quick brown fox jumps over the lazy dog.")
    await process.stdin.drain()
    process.stdin.close()
    await process.wait()

    # The interesting thing about using the shell is the additional stuff it
    # provides such as env var expansion, etc:
    print("=" * 80)
    process = await asyncio.create_subprocess_shell(
        "ls ~",
        stdout=asyncio.subprocess.PIPE,
    )
    line = await process.communicate()
    print(f"{line=}")


if __name__ == "__main__":
    # Start the event loop in a separate subprocess
    asyncio.run(main())
