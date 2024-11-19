"""Playing with the client interface of aiohttp to make requests."""

import asyncio

import aiohttp


async def main() -> None:
    """Make a HTTP request to a site asynchronously."""
    # Regular HTTP get request
    async with (
        aiohttp.ClientSession(trust_env=True) as session,
        session.get("https://example.com") as resp,
    ):
        print(resp.status)
        print(await resp.text())

    # Making websocket request
    async with (
        aiohttp.ClientSession(trust_env=True) as session,
        session.ws_connect("wss://echo.websocket.org/") as ws,
    ):
        n = 0
        print(f"Sending 'hello{n}'")
        await ws.send_str(f"hello{n}")
        async for msg in ws:
            print(f"Received '{msg.data}'")

            n += 1
            print(f"Sending 'hello{n}'")
            await ws.send_str(f"hello{n}")
            if n == 10:  # noqa: PLR2004
                return


if __name__ == "__main__":
    asyncio.run(main())
