"""Illustrates how to use asyncio stream to check HTTP status."""

import asyncio
import contextlib
import time
from urllib.parse import urlsplit


async def get_status(url: str) -> int:
    """Get HTTP status code of the given url."""
    url_parsed = urlsplit(url)
    if url_parsed.scheme == "https":
        reader, writer = await asyncio.open_connection(
            url_parsed.hostname,
            443,
            ssl=True,
        )
    else:
        reader, writer = await asyncio.open_connection(url_parsed.hostname, 80)

    # Prepare HEAD request
    query = f"HEAD {url_parsed.path} HTTP/1.1\r\nHost: {url_parsed.hostname}\r\n\r\n"

    # Write request into the socket
    writer.write(query.encode())

    # Wait for the bytes to be effectively sent down the wire
    await writer.drain()

    # Read the single line response
    response_bytes = await reader.readline()

    # Close the socket and underlying StreamWriter
    # Because we're not doing anything else, we can skip the
    # writer.wait_closed()
    writer.close()

    # Manually decoding the response
    status = response_bytes.decode().strip()

    # Return the decoded status code
    return status  # noqa: RET504


async def get_url_status(url: str) -> tuple[str, int]:
    """Thin wrapper over get_status that return also the URL."""
    try:
        status = await get_status(url)
    except OSError as e:
        return url, str(e)
    else:
        return url, status


async def main() -> None:
    """Async entry point."""
    # Sequentially checking for website status
    start = time.perf_counter()
    urls = [
        "https://google.com/",
        "http://example.com/",
        "https://example.com/",
        "http://localhost:5000/",
        "https://jwt.ms",  # note the missing /
    ]
    for url in urls:
        try:
            status = await get_status(url)
        except OSError as e:
            status = str(e)
        finally:
            print(f"{url:30}:\t{status}")
    print(f"Process took {time.perf_counter() - start:.3f} second(s)")

    # Checking websites concurrently with asyncio.gather
    print("=" * 80)
    start = time.perf_counter()
    tasks = [asyncio.create_task(get_status(url)) for url in urls]
    future = asyncio.gather(*tasks, return_exceptions=True)
    if not future.done():
        try:
            await future
        finally:
            for url, result in zip(urls, future.result(), strict=False):
                print(f"{url:30}:\t{result}")
    print(f"Process took {time.perf_counter() - start:.3f} second(s)")

    # Checking websites concurrently with asyncio.TaskGroup just won't work
    # because tasks are cancelled when the first task fails
    # print("=" * 80)
    # results = []
    # try:
    #     async with asyncio.TaskGroup() as group:
    #         tasks = [
    #             group.create_task(asyncio.shield(get_status(url))) for url in urls
    #         ]
    #         for task in tasks:
    #             try:
    #                 result = await task
    #                 results.append(result)
    #             except OSError as e:
    #                 results.append(str(e))
    # except Exception as e:
    #     print(f"Exception: {e}")

    # for url, result in zip(urls, results, strict=True):
    #     if not task.exception():
    #         print(f"{url:30}:\t{result}")

    # as_completed can also be used to get results as they happen, but you'll
    # need an enhanced version of get_satus that also returns the URL as you'll
    # get the results unsorted.
    print("=" * 80)
    start = time.perf_counter()
    tasks = [asyncio.create_task(get_url_status(url)) for url in urls]
    for aw in asyncio.as_completed(tasks):
        url, status = await aw
        print(f"{url}:\t{status}")

    print(f"Process took {time.perf_counter() - start:.3f} second(s)")


if __name__ == "__main__":
    asyncio.run(main())
