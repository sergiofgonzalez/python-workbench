"""Illustrate the Observer pattern implemented in Python."""

import asyncio


class NamedEvent(asyncio.Event):
    """Subclassed Event featuring a name."""

    def __init__(self, name: str) -> None:
        """Initialize NamedEvent instance."""
        if not name:
            msg = "a named event must have a name"
            raise ValueError(msg)
        self._name = name
        super().__init__()

    @property
    def name(self) -> str:
        """Return the name of the event."""
        return self._name


class EventEmitter:
    """The subject of the Observer pattern."""

    def __init__(self) -> None:
        """Initialize an EventEmitter instance."""
        self.evt_registry: dict[str, NamedEvent] = {}
        self.cb_registry: dict[str, list[asyncio.Task]] = {}

    def register_listener(self, evt: str) -> None:
        """Register a new (dummy) event listener."""
        if evt not in self.evt_registry:
            self.evt_registry[evt] = NamedEvent(evt)
            self.cb_registry[evt] = []
        named_event = self.evt_registry[evt]
        waiter_task = asyncio.create_task(listener_fn(named_event))
        self.cb_registry[evt].append(waiter_task)

    def emit(self, evt: str) -> None:
        """Fire an event by its name."""
        if named_evt := self.evt_registry.get(evt):
            named_evt.set()
        else:
            print(
                ">> (warning) There was no such event in the registry for this event emitter"  # noqa: COM812, E501
            )


async def listener_fn(event: NamedEvent) -> None:
    """Actions to be performed when event is triggered."""
    print(f">> listener established for {event.name}")
    await event.wait()
    print(f">> callback associated to {event.name} fired!")


async def main() -> None:
    """Application entry point."""
    event_emitter = EventEmitter()
    event_emitter.register_listener("quick")
    event_emitter.register_listener("slow")
    event_emitter.register_listener("never")


    # sleep for 1/2 second and set the event2
    await asyncio.sleep(0.5)
    event_emitter.emit("quick")

    # sleep for 1 second and set the event1
    await asyncio.sleep(0.25)
    event_emitter.emit("slow")


asyncio.run(main())
