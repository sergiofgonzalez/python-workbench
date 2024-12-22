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

    async def listener_fn(
        self,
        event: NamedEvent,
        cb: callable,
    ) -> None:
        """Wrap the actions to be performed when event is triggered."""
        print(f">> listener established for {event.name}")
        await event.wait()
        print(">> Re-establishing the listeners for further events of the same type.")
        for listener in self.cb_registry[event.name]:
            listener()
        print(f">> callback associated to {event.name} fired!")
        cb(*event.args, **event.kwargs)

    def __init__(self) -> None:
        """Initialize an EventEmitter instance."""
        self.evt_registry: dict[str, NamedEvent] = {}
        self.cb_registry: dict[str, list[asyncio.Task]] = {}
        self.background_tasks = set()

    def register_listener(self, evt: str, cb: callable) -> None:
        """Register an event listener to be called when the event is fired."""

        def re_register_waiter_task() -> asyncio.Task:
            """Call to re-establish the waiter task."""
            return asyncio.create_task(self.listener_fn(named_event, cb))

        if evt not in self.evt_registry:
            self.evt_registry[evt] = NamedEvent(evt)
            self.cb_registry[evt] = []
        named_event = self.evt_registry[evt]
        waiter_task = asyncio.create_task(self.listener_fn(named_event, cb))

        # some housekeeping to control dangling tasks
        self.background_tasks.add(waiter_task)

        # when task is done, remove its own reference from the set of tasks
        waiter_task.add_done_callback(self.background_tasks.discard)

        self.cb_registry[evt].append(re_register_waiter_task)

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


def find_regex(file_list: list[str], search_str: str) -> EventEmitter:
    """Scan the files in file_list searching for the regex."""

    async def do_search_match() -> None:
        print(">>> About to start scanning")
        for file_path in file_list:
            print(f">>> scanning {file_path}")
            for line in Path.open(file_path, "r"):
                if result := regex.search(line):
                    event_emitter.emit("found", file_path, result.group())

    event_emitter = EventEmitter()
    regex = re.compile(search_str)
    task = asyncio.create_task(do_search_match())
    return event_emitter, task


async def main() -> None:
    """Application entry point."""
    event_emitter, task = find_regex(
        ["file.txt", "pyproject.toml", "README.md"], r"(H|h)ello",
    )
    event_emitter.register_listener(
        "found",
        lambda file, match: print(f"Matched {match!r} in {file!r}"),
    )
    if not task.done():
        print(">>> task not done yet")
        await task



if __name__ == "__main__":
    # regex = re.compile(r".*(H|h)ello.*")
    # with Path.open("file.txt", "r") as f:
    #     for line in f:
    #         result = regex.match(line)
    #         if result:
    #             print(result.group())
    asyncio.run(main())
