"""Using events with data to manage subscriptions à la Node.js."""

import asyncio


class NamedEvent(asyncio.Event):
    """Named Event Class."""

    def __init__(self, name: str) -> None:
        """Initialize NamedEvent class."""
        super().__init__()
        self.name = name


async def register_event_handler(
    event: NamedEvent,
    client_id: str,
    action: callable,
) -> None:
    """Handle the event when fired."""
    # block until the event is fired
    await event.wait()
    print(f"Got event {event.name!r} for client {client_id}")
    action()


async def emit_event(event: asyncio.Event, delay_seconds: float = 0) -> None:
    """Trigger an event after some delay."""
    await asyncio.sleep(delay_seconds)
    event.set()


def announce_join_fn(
    client: str,
    message: str,
    *args: any,
    **kwargs: dict[str, any],
) -> None:
    """Announce that join event has been received."""

    def fn() -> None:
        print(f"join event received for {client=}: {message!r}")

    return fn


def handle_broadcast(client: str, message: str) -> None:
    """Handle the broadcast event."""

    def fn() -> None:
        print(f"broadcast event received for {client=}: {message!r}")

    return fn


async def main() -> None:
    """Async entry point."""
    # Create Event object
    join_event = NamedEvent("join")
    broadcast_event = NamedEvent("broadcast")
    leave_event = NamedEvent("leave")
    shutdown_event = NamedEvent("shutdown")

    # Simulate a client that joins the chat server and subscribe to the
    # different events
    client_id = "client_1"

    # Establish the subscriptions
    handlers = [
        asyncio.create_task(
            register_event_handler(
                join_event,
                client_id,
                announce_join_fn(client_id, "hello, join for client_1"),
            ),
        ),
        asyncio.create_task(
            register_event_handler(
                broadcast_event,
                client_id,
                handle_broadcast(client_id, "broadcasted message"),
            ),
        ),
    ]


    # Simulate a client that joins the chat server and do not subscribe to the
    # broadcast
    client_id = "client_2"
    handlers.append(
        asyncio.create_task(
            register_event_handler(
                join_event,
                client_id,
                announce_join_fn(client_id, "hello, join for client_2"),
            ),
        ),
    )

    await emit_event(join_event)
    await emit_event(broadcast_event, 3)

    await asyncio.gather(*handlers)


if __name__ == "__main__":
    asyncio.run(main())
