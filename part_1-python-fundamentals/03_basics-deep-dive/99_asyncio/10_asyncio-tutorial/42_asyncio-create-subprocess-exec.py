"""
Illustrate how to use asyncio.create_subprocess_exec().

In the example, we execute the `echo` command that reports back the string
passed as a parameter, in the stdout.
"""

import asyncio


async def main() -> None:
    """Async Main coroutine."""
    # Start executing a command in a separate subprocess
    # Output will be displayed in the command line automatically
    process = await asyncio.create_subprocess_exec("echo", "Hello, world")
    print(f"subprocess: {process}")

    # Start executing a command in a separate subprocess, piping stdout
    print("=" * 80)
    process = await asyncio.create_subprocess_exec(
        "echo",
        "Hello, world",
        stdout=asyncio.subprocess.PIPE,
    )
    # read a line from the process output stream
    line = await process.stdout.readline()
    print(f"{line=}")

    # Start executing a command in a separate subprocess, piping stdin
    print("=" * 80)
    process = await asyncio.create_subprocess_exec(
        "wc",
        "-c",
        stdin=asyncio.subprocess.PIPE,
    )
    # send some data to the process input stream
    await process.communicate(input=b"the quick brown fox")

    # Start executing a command in a separate subprocess, piping stdin and
    # communicate using streamwriter methods
    print("=" * 80)
    process = await asyncio.create_subprocess_exec(
        "wc",
        "-c",
        stdin=asyncio.subprocess.PIPE,
    )
    # send some data to the process input stream using the StreamWriter
    process.stdin.write(b"the quick brown fox jumps over the lazy dog.")
    await process.stdin.drain()
    process.stdin.close()
    await process.wait()



if __name__ == "__main__":
    # Start the event loop in a separate subprocess
    asyncio.run(main())
