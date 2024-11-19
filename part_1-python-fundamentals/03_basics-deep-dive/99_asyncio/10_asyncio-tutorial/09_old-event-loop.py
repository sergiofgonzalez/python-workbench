"""Illustrating how to interact with the event loop the old-fashioned way."""

import asyncio


def hello_world(loop: asyncio.AbstractEventLoop) -> None:
    """Print 'Hello, world' and stop the event loop callback-style."""
    print("Hello, world!")
    loop.stop()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.call_soon(hello_world, loop)

    try:
        loop.run_forever()
    finally:
        loop.close()
