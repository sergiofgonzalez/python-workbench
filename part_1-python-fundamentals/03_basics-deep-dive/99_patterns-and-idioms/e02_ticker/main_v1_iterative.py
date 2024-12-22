"""Ticker: a function that returns the number of ticks."""

import asyncio
import time

from events import EventEmitter

MILLISECONDS_PER_SECOND = 1000
FIFTY_MILLISECONDS = 0.05


class Ticker(EventEmitter):
    """Class that emits a tick every 50 msecs until a given time expires."""

    def __init__(self, duration_millis: int, done_cb: callable) -> None:
        """Initialize with the expiration time and cb to invoke at the end."""
        super().__init__()
        self.duration_seconds = duration_millis / MILLISECONDS_PER_SECOND
        self.done_cb = done_cb
        self.num_ticks = 0

    async def start(self) -> None:
        """Start the ticking process."""
        start_ts = time.perf_counter()
        done = False
        while not done:
            now_ts = time.perf_counter()
            await asyncio.sleep(FIFTY_MILLISECONDS)
            if now_ts - start_ts > self.duration_seconds:
                done = True
                self.done_cb(self.num_ticks)
            else:
                self.num_ticks += 1
                self.emit("tick")


async def main() -> None:
    """Application entry point."""
    ticker = Ticker(1500, lambda num_ticks: print(f"Time elapsed! {num_ticks=}"))
    ticker.register_listener("tick", lambda: print("tick"))
    start_ts = time.perf_counter()
    await ticker.start()
    print(f"Total duration: {time.perf_counter() - start_ts:0.3f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
