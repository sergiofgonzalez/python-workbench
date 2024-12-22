"""Illustrate the Observer pattern implemented in Python."""

import asyncio
import re
from pathlib import Path


class NamedEvent(asyncio.Event):
    """Subclassed Event featuring a name."""

    def __init__(self, name: str) -> None:
        """Initialize NamedEvent instance."""
        if not name:
            msg = "a named event must have a name"
            raise ValueError(msg)
        self._name = name
        self.args = None
        self.kwargs = None
        super().__init__()

    @property
    def name(self) -> str:
        """Return the name of the event."""
        return self._name


class EventEmitter:
    """The subject of the Observer pattern."""

    @staticmethod
    async def listener_fn(
        event: NamedEvent,
        cb: callable,
    ) -> None:
        """Wrap the actions to be performed when event is triggered."""
        print(f">> listener established for {event.name}")
        await event.wait()
        print(f">> callback associated to {event.name} fired!")
        cb(event.args, event.kwargs)

    def __init__(self) -> None:
        """Initialize an EventEmitter instance."""
        self.evt_registry: dict[str, NamedEvent] = {}
        self.cb_registry: dict[str, list[asyncio.Task]] = {}

    def register_listener(self, evt: str, cb: callable) -> None:
        """Register an event listener to be called when the event is fired."""
        if evt not in self.evt_registry:
            self.evt_registry[evt] = NamedEvent(evt)
            self.cb_registry[evt] = []
        named_event = self.evt_registry[evt]
        waiter_task = asyncio.create_task(self.listener_fn(named_event, cb))
        self.cb_registry[evt].append(waiter_task)

    def emit(self, evt: str, *args: tuple, **kwargs: dict) -> None:
        """Fire an event by its name."""
        if named_evt := self.evt_registry.get(evt):
            named_evt.args = args
            named_evt.kwargs = kwargs
            named_evt.set()
        else:
            print(
                ">> (warning) There was no such event in the registry for this event emitter"  # noqa: COM812, E501
            )


async def main() -> None:
    """Application entry point."""
    event_emitter = EventEmitter()
    event_emitter.register_listener(
        "quick",
        lambda args, kwargs: print(f"{args=}, {kwargs=}"),
    )
    event_emitter.register_listener(
        "slow",
        lambda args, kwargs: print(f"{args=}, {kwargs=}"),
    )
    event_emitter.register_listener(
        "never",
        lambda args, kwargs: print(f"{args=}, {kwargs=}"),
    )

    # sleep for 1/2 second and set the event2
    await asyncio.sleep(0.5)
    event_emitter.emit(
        "quick",
        "this",
        "was",
        "a ",
        "quick",
        "event",
        duration=0.5,
    )

    # sleep for 1 second and set the event1
    await asyncio.sleep(0.25)
    event_emitter.emit(
        "slow",
        "this",
        "was",
        "a ",
        "slow",
        "event",
        duration=0.25,
    )
    event_emitter.emit("slow", "wait", "I'm overwriting the prev one")

    await asyncio.sleep(0.25)
    event_emitter.emit(
        "slow",
        "this",
        "was",
        "a ",
        "slow",
        "event",
        duration=0.25,
    )


if __name__ == "__main__":
    regex = re.compile(r".*(H|h)ello.*")
    # with Path.open("file.txt", "r") as f:
    #     for line in f:
    #         result = regex.match(line)
    #         if result:
    #             print(result.group())
    asyncio.run(main())
