"""Telnet chat server written with asyncio sockets."""

import asyncio
import os
import signal
import sys

PORT = os.getenv("CHAT_PORT", "8888")

MAX_CLIENTS = 2
clients = {}


def get_client_id(writer: asyncio.StreamWriter) -> str:
    """Compute and return the client_id for a new client connection."""
    client_remote_address, client_remote_port = writer.get_extra_info(
        "peername",
    )
    return f"{client_remote_address}:{client_remote_port}"


async def send_message(client_id: str, message: str) -> None:
    """Send a message to the corresponding registered client."""
    message_bytes = message.encode()
    _, writer = clients[client_id]
    writer.write(message_bytes)
    await writer.drain()


async def broadcast_message(sender_id: str, message: str) -> None:
    """Broadcast a message to all connected clients but the sender."""
    broadcast_tasks = [
        asyncio.create_task(send_message(client_id, message))
        for client_id in clients
        if client_id != sender_id
    ]
    await asyncio.gather(*broadcast_tasks)


async def disconnect_client(
    client_id: str,
    disconnect_msg: str = "",
) -> None:
    """Handle housekeeping tasks on client disconnect (abruptly or normally)."""
    if disconnect_msg:
        await send_message(client_id, disconnect_msg)
    _, writer = clients[client_id]
    del clients[client_id]
    writer.close()
    await writer.wait_closed()
    print(f"client: {client_id} has been disconnected.")


async def handle_new_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    server: asyncio.AbstractServer,
) -> None:
    """Handle incoming requests from clients."""
    client_id = get_client_id(writer)

    print(f"A new connection request has been received: {client_id}")
    clients[client_id] = (reader, writer)
    if len(clients) > MAX_CLIENTS:
        message = "Apologies: The chat server is full. Please try again later."
        await disconnect_client(client_id, message)
        return

    welcome_message = (
        "Congratulations! You've successfully joined the chat server.\n"
        f"Your id is: {client_id!r}.\n"
        f"There are {len(clients)} client(s) connected to this server.\n"
    )
    await send_message(client_id, welcome_message)

    try:
        while True:
            data = await reader.read(255)
            if not data:
                print("Client has disconnected")
                break
            try:
                data_str = data.decode()
            except UnicodeDecodeError:
                msg = f"ERROR: client {client_id!r} sent a message that couldn't be decoded: will ignore"  # noqa: E501
                print(msg)
                await send_message(
                    client_id,
                    "SERVER: Hey, your latest message has been ignored",
                )
            else:
                if data_str.strip() == "SHUTDOWN":
                    print(
                        f"'SHUTDOWN' event received from client {client_id!r}"
                    )
                    message = "Shutting down chat server."
                    await broadcast_message(client_id, data_str)
                    shutdown_task = asyncio.create_task(handle_shutdown(server))
                    await shutdown_task
                await broadcast_message(client_id, data_str)

    except Exception as e:  # noqa: BLE001
        print(f"ERROR: {client_id}: {e} ({type(e)})")
        message = f"Disconnecting {client_id!r} because connection was broken."
        await disconnect_client(client_id, message)


async def handle_shutdown(server: asyncio.AbstractServer) -> None:
    """Shutdown the server and client connections."""
    print("Shutting down server")
    server.close()
    await server.wait_closed()
    for client_id, (_, writer) in clients.items():
        print(f"Closing {client_id!r}")
        writer.close()
        await writer.wait_closed()
    clients.clear()
    print("Server closed.")


async def main() -> None:
    """Async entry point."""
    server = await asyncio.start_server(
        lambda r, w: handle_new_client(r, w, server),
        host="127.0.0.1",
        port=PORT,
    )

    async with server:
        print(f"Chat server started: waiting for connections on port {PORT}")

        # Register signal handlers for graceful shutdown
        loop = asyncio.get_running_loop()
        for sig in [signal.SIGINT, signal.SIGTERM]:
            loop.add_signal_handler(
                sig,
                lambda: asyncio.create_task(handle_shutdown(server)),
            )
        try:
            await server.serve_forever()
        except asyncio.CancelledError:
            print("Server was cancelled.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCTRL-C received: closing the application")
        sys.exit(1)
    print("Server closed.")
