"""An async web crawler written in Python."""

import asyncio

from spider import spider

url = "https://www.imdb.com/title/tt0049096"
nesting = 1
concurrency = 2


async def main() -> None:
    """Async application entry point."""
    try:
        await spider(url, nesting, concurrency)
    except Exception as e:  # noqa: BLE001
        print(f"ERROR downloading {url}: {e} ({type(e)})")


if __name__ == "__main__":
    asyncio.run(main())
