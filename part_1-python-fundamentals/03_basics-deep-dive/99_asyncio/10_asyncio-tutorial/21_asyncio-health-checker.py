"""Illustrate how to efficiently implement a health checker for websites."""

import asyncio
import time

import aiohttp
import requests

HTTP_OK_THRESHOLD = 400


def check_url(url: str) -> int:
    """
    Return the status code of an HTTP HEAD request on the URL.

    If the URL does not respond after 5 seconds it times out.
    """
    resp = requests.head(url, allow_redirects=True, timeout=(5, 5))
    return resp.status_code


async def check_url_async(session: aiohttp.ClientSession, url: str) -> int:
    """
    Return the status code of an HTTP HEAD request on the URL.

    If the URL does not respond after 5 seconds it times out.
    """
    try:
        async with session.head(url, timeout=5) as resp:
            return resp.status
    except aiohttp.ClientError:
        return -1


def url_checker_sync(*urls: str) -> None:
    """
    Check that the websites identified by those URLs are responding with
    status codes below 400.
    """
    start_proc = time.perf_counter()
    for url in urls:
        print(f"HEAD {url} =>", end=" ", flush=True)
        try:
            start = time.perf_counter()
            status = check_url(url)
            end = time.perf_counter() - start
            if status < HTTP_OK_THRESHOLD:
                print(f"OK ({end:0.3f}s)")
            else:
                print(f"ERROR ({status}) ({end:0.3f}s)")
        except requests.RequestException:
            end = time.perf_counter() - start
            print(f"ERROR (RequestException) ({end:0.3f}s)")
    end = time.perf_counter() - start_proc
    print(f"Total time: {end:0.3f}s")


async def url_checker_async(*urls: str) -> None:
    """
    Check that the websites identified by those URLs are responding with
    status codes below 400.
    """
    start = time.perf_counter()
    async with aiohttp.ClientSession(trust_env=True) as session:
        results = await asyncio.gather(
            *[check_url_async(session, url) for url in urls],
        )
        for url, result in zip(urls, results, strict=True):
            if result >= 0 and result < HTTP_OK_THRESHOLD:
                print(f"HTTP HEAD {url} => OK")
            elif result >= HTTP_OK_THRESHOLD:
                print(f"HTTP HEAD {url} ERROR ({result})")
            else:
                print(f"HTTP HEAD {url} EXCEPTION")
    end = time.perf_counter() - start
    print(f"Total time: {end:0.3f}s")


if __name__ == "__main__":
    print("Sync version:")
    url_checker_sync(
        "https://github.com",
        "https://example.com",
        "https://this-web-does-not-exist.com",
        "http://localhost",
    )
    print("Async version:")
    asyncio.run(
        url_checker_async(
            "https://github.com",
            "https://example.com",
            "https://this-web-does-not-exist.com",
            "http://localhost",
        ),
    )
