"""A simple socket chat server using asyncio."""

import asyncio

from rich import print


async def handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
) -> None:
    """Handle the connection request from a client."""
    # Read up to 100 bytes from the stream
    data = await reader.read(100)
    message = data.decode()
    address = writer.get_extra_info("peername")

    print(f"Received {message!r} from {address!r}")
    out_message = message.upper()
    out_message_bytes = out_message.encode()
    print(f"Sending: {out_message}")
    writer.write(out_message_bytes)
    await writer.drain()

    print("Closing the connection")
    writer.close()
    await writer.wait_closed()


async def main() -> None:
    """Async entry point."""
    # start the chat server
    print("About to start the server")
    server = await asyncio.start_server(
        handle_client,
        host="127.0.0.1",
        port=5000,
    )
    addresses = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Server started on {addresses}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    # Start the event loop in the current thread
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("CTRL-C received: closing the application")
