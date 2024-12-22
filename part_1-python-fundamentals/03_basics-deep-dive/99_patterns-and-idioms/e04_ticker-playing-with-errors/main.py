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

    def _fail_if_time_divisible_by_5(self) -> bool:
        now_millis = int(time.perf_counter() * MILLISECONDS_PER_SECOND)
        if now_millis % 5 == 0:
            self.emit("error", f"{now_millis=} is divisible by 5")
            self.done_cb(ValueError(f"{now_millis=} is divisible by 5"))
            return True
        return False

    async def _ticking_process(self, start_ts: float) -> None:
        if time.perf_counter() - start_ts > self.duration_seconds:
            self.done_cb(self.num_ticks)
        else:
            await asyncio.sleep(FIFTY_MILLISECONDS)
            self.num_ticks += 1
            self.emit("tick")
            if not self._fail_if_time_divisible_by_5():
                await self._ticking_process(start_ts)

    async def start(self) -> None:
        """Start the ticking process."""
        self.num_ticks += 1
        self.emit("tick")
        await self._ticking_process(start_ts=time.perf_counter())


def handle_done(ticks_or_exception: int | ValueError) -> None:
    """Actions when the Tick process is complete."""
    if isinstance(ticks_or_exception, int):
        print(f"Time elapsed! num_ticks={ticks_or_exception}")
    else:
        print(f"An error ocurred: {ticks_or_exception}")


async def main() -> None:
    """Application entry point."""
    ticker = Ticker(500, handle_done)
    ticker.register_listener("tick", lambda: print("tick"))
    ticker.register_listener("error", lambda e: print(f"Error: {e}"))
    start_ts = time.perf_counter()
    await ticker.start()
    print(f"Total duration: {time.perf_counter() - start_ts:0.3f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
