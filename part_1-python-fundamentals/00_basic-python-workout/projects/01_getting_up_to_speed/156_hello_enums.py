"""Illustrates the basics of enums in Python."""

from enum import Enum


class State(Enum):
    """An enumeration for different states."""

    DISABLED = 0
    ENABLED = 1


def display_state(state: State) -> None:
    """Display the state."""
    if state == State.ENABLED:
        print("State is enabled.")
    elif state == State.DISABLED:
        print("State is disabled.")
    else:
        print("Unknown state.")


def main() -> None:
    """Application entry point."""
    print("State.ENABLED:", State.ENABLED)
    print("State.DISABLED:", State.DISABLED)

    # You can assign value as if it were a class field
    state = State.ENABLED
    display_state(state)

    # Or with this weird constructor-type syntax
    state = State(0)
    display_state(state)

    # Or as if it were a dict
    state = State["ENABLED"]
    display_state(state)

    # You can access the value using the '.' syntax
    print(f"{state.value}")
    print(f"{State.DISABLED.value}")
    print(f"{State.ENABLED.value}")

    # You can get a list of all the values in the enum with list()
    print(f"{list(State)=}, number of values: {len(State)=}")



if __name__ == "__main__":
    main()
