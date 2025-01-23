"""Web crawling functions."""

import aiofiles
from utils import url_to_filename
from work_queue import WorkQueue

spidering = set()


async def download(url, filename):
    return "content"


def get_content_fn(url, filename):
    async def fn():
        try:
            with aiofiles.open(filename) as f:
                content = await f.read()
        except FileNotFoundError:
            content = download(url, filename)

        return spider_links(url, content, nesting, queue)

    return fn


async def spider_task(url, nesting, work_queue: WorkQueue) -> None:
    if url in spidering:
        return
    spidering.add(url)

    filename = url_to_filename(url)
    content = work_queue.put_work_item(get_content_fn())


async def spider(url: str, nesting: int, concurrency: int) -> None:
    await spider_task(url, nesting, WorkQueue(concurrency))
