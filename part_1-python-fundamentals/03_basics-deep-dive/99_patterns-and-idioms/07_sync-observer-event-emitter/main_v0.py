"""A custom sync implementation of the Observer pattern."""


class EventEmitter:
    """The subject of the Observer pattern."""

    def __init__(self) -> None:
        """Initialize an EventEmitter object."""
        self.listeners: dict[str, list[callable]] = {}

    def register_listener(self, evt_name: str, cb: callable) -> None:
        """Register a new observer (listener) in this event emitter."""
        if evt_name not in self.listeners:
            self.listeners[evt_name] = [cb]
        else:
            self.listeners[evt_name].append(cb)

    def emit(self, evt_name: str, *args: tuple, **kwargs: dict) -> None:
        """Fire an event by name with the given details."""
        for cb in self.listeners.get(evt_name, []):
            cb(*args, **kwargs)

    def remove_listener(self, evt_name: str, cb: callable) -> None:
        """Remove listener for the given event."""
        if evt_name in self.listeners:
            self.listeners[evt_name].remove(cb)
        else:
            msg = "No such event registered in this event emitter."
            raise ValueError(msg)


def main() -> None:
    """Application entry point."""

    def handle_evt(*args: tuple, **kwargs: dict) -> None:
        print(f"one-handler-2: {args}, {kwargs}")

    event_emitter = EventEmitter()
    event_emitter.register_listener(
        "one",
        lambda *args, **kwargs: print(f"one-handler-1: {args}, {kwargs}"),
    )
    event_emitter.register_listener(
        "one",
        handle_evt,
    )
    event_emitter.register_listener(
        "two",
        lambda *args, **kwargs: print(f"two-handler-1: {args}, {kwargs}"),
    )

    # Firing an event with no handler
    event_emitter.emit("three")

    # Firing an event with two handlers
    event_emitter.emit(
        "one",
        "some",
        "param",
        named_kwarg_1="kwarg_1-val",
        named_kwarg_2="kwarg_2-val",
    )
    event_emitter.emit(
        "one",
        "other",
        "event",
        named_kwarg_3="kwarg_3-val",
        named_kwarg_4="kwarg_4-val",
    )

    # Firing an event with a single handler
    event_emitter.emit(
        "two",
        "fired",
        "two",
        named_kwarg_5="kwarg_5-val",
    )

    # Remove a handler
    event_emitter.remove_listener("one", handle_evt)
    event_emitter.emit(
        "one",
        "param",
        named_kwarg_6="kwarg_6-val",
    )



if __name__ == "__main__":
    main()
