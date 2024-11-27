"""Telnet chat server written with asyncio sockets."""

import asyncio
import os
import sys

PORT = os.getenv("CHAT_PORT", "8888")

clients = {}


async def handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
) -> None:
    """Handle incoming requests from clients."""
    client_remote_address, client_remote_port = writer.get_extra_info(
        "peername",
    )
    client_id = f"{client_remote_address}:{client_remote_port}"
    print(f"A new connection request has been received: {client_id}")
    clients[id] = (reader, writer)

    welcome_message = f"""
    Congratulations! You've successfully joined the chat server.
    Your id is {client_id!r}.
    There are {len(clients)} client(s) currently connected to the chat.
    """.strip()
    welcome_message_bytes = welcome_message.encode()
    writer.write(welcome_message_bytes)
    await writer.drain()

    while True:
        data = await reader.read()
        data_str = data.decode()
        print(f"{client_id}: received message: {data_str!r}")
        if data_str == "leave":
            print(f"Closing the connection for client: {client_id}")
            writer.close()
            await writer.wait_closed()
            del clients[client_id]


async def main() -> None:
    """Async entry point."""
    server = await asyncio.start_server(
        handle_client,
        host="127.0.0.1",
        port=PORT,
    )

    async with server:
        print(f"Chat server started: waiting for connections on port {PORT}")
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCTRL-C received: closing the application")
        sys.exit(0)
