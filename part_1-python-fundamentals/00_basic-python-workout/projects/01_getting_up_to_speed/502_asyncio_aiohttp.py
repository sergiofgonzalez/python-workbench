"""Illustrates how to use aiohttp for asynchronous HTTP requests."""

import asyncio

import aiohttp


async def main() -> None:
    """Async application entry point."""
    # Simple HTTP GET request example using aiohttp
    async with (
        aiohttp.ClientSession() as session,
        session.get("https://example.com") as response,
    ):
        print("Status:", response.status)
        print("Content-type:", response.headers["content-type"])
        html = await response.text()
        print("Body:", html[:100], "...")
    print("=" * 40)

    # WSS: Simple websocket example using aiohttp
    async with (
        aiohttp.ClientSession() as session,
        session.ws_connect("wss://echo.websocket.org/") as ws,
    ):
        await ws.send_str("Hello, WebSocket!")
        msg = await ws.receive()

        if msg.type == aiohttp.WSMsgType.TEXT:
            print("Received:", msg.data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print("WebSocket error:", msg.data)
    print("=" * 40)

    # WSS: You can use async for to receive messages in a loop
    async with (
        aiohttp.ClientSession() as session,
        session.ws_connect("wss://echo.websocket.org/") as ws,
    ):
        i = 0
        print(f"Sending first 'hello {i}' using websockets")
        await ws.send_str(f"hello {i}")
        async for msg in ws:
            print("in async for loop")
            if msg.type == aiohttp.WSMsgType.TEXT:
                print("Received in loop:", msg.data)
                print(f"Sending 'hello {i}' using websockets")
                await ws.send_str(f"hello {i}")
                i += 1
                if i >= 5:  # noqa: PLR2004
                    print("Sent 5 messages, closing websocket")
                    break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print("WebSocket error in loop:", msg.data)
                break
    print("WebSocket closed")
    print("=" * 40)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
