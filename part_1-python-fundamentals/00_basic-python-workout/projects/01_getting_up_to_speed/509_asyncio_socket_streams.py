"""Illustrates how to use asyncio socket streams to implement a simple HTTP."""

import asyncio
import logging
import time

import urllib3

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


async def get_status(url: str) -> int:
    """Get the HTTP status code for a given URL after sending a HEAD request."""
    url_obj = urllib3.util.parse_url(url)  # validate URL format
    logger.debug("Parsed URL: %s", url_obj)

    if url_obj.scheme == "https":
        logger.info("Establishing HTTPS connection to %s on port 443", url_obj.host)
        reader, writer = await asyncio.open_connection(url_obj.host, 443, ssl=True)
    else:
        logger.info("Establishing HTTP connection to %s on port 80", url_obj.host)
        reader, writer = await asyncio.open_connection(url_obj.host, 80)
    logger.info("Connection established to %s", url_obj.host)

    head_request_str = (
        f"HEAD /{url_obj.path} HTTP/1.1\r\n"
        f"Host: {url_obj.host}\r\n"
        "Connection: close\r\n\r\n"
    )
    writer.write(head_request_str.encode("utf-8"))
    await writer.drain()
    logger.info("Sent HEAD request to %s/%s", url_obj.host, url_obj.path)

    status_line_bytes = await reader.readline()
    writer.close()
    await writer.wait_closed()
    logger.info("Connection closed to %s", url_obj.host)

    # Example status line: "HTTP/1.1 200 OK"
    status_line = status_line_bytes.decode("utf-8").strip().split("\r\n")[0]
    status_code = int(status_line.split(" ")[1])
    logger.info("Received status line: %s; status code=%d", status_line, status_code)
    return status_code


async def get_url_status(url: str) -> tuple[str, int | str]:
    """Wrap invocation of get_status."""
    try:
        status_code = await get_status(url)
        return url, status_code
    except Exception as e:
        logger.exception("Error getting status for %s", url)
        return url, str(e)
    else:
        logger.info("Completed getting status for %s; code=%d", url, status_code)
        return url, status_code


async def main() -> None:
    """Async application entry point."""
    sites = [
        "https://google.com/",
        "http://example.com/",
        "https://example.com/",
        "http://localhost:5000/",
        "https://jwt.ms",  # note the missing /
    ]

    # Lab 1: sequentially checking for status codes
    start_time = time.perf_counter()
    report = []
    for site in sites:
        url, status = await get_url_status(site)
        report.append(f"{url} -> {status}")
    print("\n".join(report))
    print(f"Lab 1: sequential check: {time.perf_counter() - start_time:.3f} seconds")
    print("=" * 40)

    # Lab 2: in parallel using asyncio.gather
    start_time = time.perf_counter()
    report = []
    tasks = [get_url_status(site) for site in sites]
    results = await asyncio.gather(*tasks)
    for url, status in results:
        report.append(f"{url} -> {status}")
    print("\n".join(report))
    print(
        f"Lab 2: parallel check (gather()): {time.perf_counter() - start_time:.3f} seconds",  # noqa: E501
    )
    print("=" * 40)

    # Lab 3: in parallel using TaskGroup (Python 3.11+)
    start_time = time.perf_counter()
    report = []
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(get_url_status(site)) for site in sites]

    for task in tasks:
        url, status = task.result()
        report.append(f"{url} -> {status}")
    print("\n".join(report))
    print(
        f"Lab 3: parallel check (TaskGroup): {time.perf_counter() - start_time:.3f} seconds",  # noqa: E501
    )
    print("=" * 40)

    # Lab 4: in parallel using asyncio.as_completed
    start_time = time.perf_counter()
    report = []
    for task in asyncio.as_completed([get_url_status(site) for site in sites]):
        url, status = await task
        report.append(f"{url} -> {status}")
    print("\n".join(report))
    print(
        f"Lab 4: parallel check (as_completed): {time.perf_counter() - start_time:.3f} seconds",  # noqa: E501
    )
    print("=" * 40)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
