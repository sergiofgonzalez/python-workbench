"""A simple socket chat client using asyncio."""

import asyncio


async def main() -> None:
    """Async entry point."""
    reader, writer = await asyncio.open_connection("127.0.0.1", 5000)
    message = "Hello, chat server!"
    message_bytes = message.encode()
    print(f"Sending message: {message!r}")
    writer.write(message_bytes)
    data_bytes = await reader.read(100)
    data_str = data_bytes.decode()
    print(f"Message received: {data_str!r}")

    print("Closing the connection")
    writer.close()
    await writer.wait_closed()


if __name__ == "__main__":
    # Start the event loop in the current thread
    asyncio.run(main())
