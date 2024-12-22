"""EventEmitter: A Python implementation of the Observer pattern."""

import asyncio


class EventEmitter:
    """The subject of the Observer pattern."""

    def __init__(self) -> None:
        """Initialize an EventEmitter object."""
        self.listeners: dict[str, list[callable]] = {}
        self.background_tasks = set()

    def register_listener(self, evt_name: str, cb: callable) -> None:
        """Register a new observer (listener) in this event emitter."""
        if evt_name not in self.listeners:
            self.listeners[evt_name] = [cb]
        else:
            self.listeners[evt_name].append(cb)

    def emit(self, evt_name: str, *args: tuple, **kwargs: dict) -> None:
        """Fire an event by name with the given details."""
        for cb in self.listeners.get(evt_name, []):
            if asyncio.iscoroutinefunction(cb):
                task = asyncio.create_task(cb(*args, **kwargs))
                self.background_tasks.add(task)
                task.add_done_callback(self.background_tasks.discard)
            else:
                cb(*args, **kwargs)

    def remove_listener(self, evt_name: str, cb: callable) -> None:
        """Remove listener for the given event."""
        if evt_name in self.listeners:
            self.listeners[evt_name].remove(cb)
        else:
            msg = "No such event registered in this event emitter."
            raise ValueError(msg)
