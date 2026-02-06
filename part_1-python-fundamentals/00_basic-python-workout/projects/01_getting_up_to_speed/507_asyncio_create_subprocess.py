"""Illustrates how to run commands using asyncio.create_subprocess_exec."""

import asyncio

import rich


async def main() -> None:
    """Async application entry point."""
    # Lab 1: Execute echo "Hello, World" command, expecting no output capture
    # (output goes to the terminal)
    process = await asyncio.create_subprocess_exec(
        "echo",
        "Hello, World",
    )
    rich.print(f"[yellow]>>> [{process.pid}] started[/yellow]")
    print(process)

    # wait for the process to complete
    await process.wait()
    rich.print(
        f"[yellow]>>> [{process.pid}] completed: returncode={process.returncode}[/yellow]",  # noqa: E501
    )
    print("=" * 40)

    # Lab 2: Execute echo "Hello, World" command, capturing stdout and stderr
    process = await asyncio.create_subprocess_exec(
        "echo",
        "Hello, World",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    rich.print(f"[yellow]>>> [{process.pid}] started[/yellow]")

    # reading the output and printing the output using decode
    stdout, stderr = await process.communicate()
    print(f"[stdout]\n{stdout.decode()!r}")
    print(f"[stderr]\n{stderr.decode()!r}")

    # wait for the process to complete
    await process.wait()
    rich.print(
        f"[yellow]>>> [{process.pid}] completed: returncode={process.returncode}[/yellow]",  # noqa: E501
    )
    print("=" * 40)

    # Lab 3: Execute echo "Hello, World" command, capturing stdout and stderr and
    # reading output line by line
    process = await asyncio.create_subprocess_exec(
        "echo",
        "Hello, World\nThis is a test.\nGoodbye!",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    rich.print(f"[yellow]>>> [{process.pid}] started[/yellow]")

    # reading the output line by line (do NOT call communicate() first!)
    while True:
        line = await process.stdout.readline()  # type:ignore[union-attr]
        if not line:
            break
        print(f"line: {line.decode()!r}")

    # wait for the process to complete after reading all output
    await process.wait()
    rich.print(
        f"[yellow]>>> [{process.pid}] completed: returncode={process.returncode}[/yellow]",  # noqa: E501
    )
    print("=" * 40)

    # Lab 4: piping stdin to the subprocess and sending data with communicate
    process = await asyncio.create_subprocess_exec(
        "wc",
        "-c",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    rich.print(f"[yellow]>>> [{process.pid}] started[/yellow]")
    # sending input to stdin and reading output
    stdout, stderr = await process.communicate(input=b"Hello to Jason Isaacs!")
    print(f"[stdout]\n{stdout.decode()!r}")
    print(f"[stderr]\n{stderr.decode()!r}")

    # wait for the process to complete after reading all output
    await process.wait()
    rich.print(
        f"[yellow]>>> [{process.pid}] completed: returncode={process.returncode}[/yellow]",  # noqa: E501
    )
    print("=" * 40)

    # Lab 5: piping stdin to the subprocess and sending data through stdin.write
    process = await asyncio.create_subprocess_exec(
        "wc",
        "-c",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    rich.print(f"[yellow]>>> [{process.pid}] started[/yellow]")
    # sending input to stdin and reading output
    process.stdin.write(b"Hello to Jason Isaacs!")  # ty:ignore[possibly-missing-attribute]
    await process.stdin.drain()  # ty:ignore[possibly-missing-attribute]
    process.stdin.close()  # ty:ignore[possibly-missing-attribute]
    stdout, stderr = await process.communicate()
    print(f"[stdout]\n{stdout.decode()!r}")
    print(f"[stderr]\n{stderr.decode()!r}")

    # wait for the process to complete after reading all output
    await process.wait()
    rich.print(
        f"[yellow]>>> [{process.pid}] completed: returncode={process.returncode}[/yellow]",  # noqa: E501
    )
    print("=" * 40)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
