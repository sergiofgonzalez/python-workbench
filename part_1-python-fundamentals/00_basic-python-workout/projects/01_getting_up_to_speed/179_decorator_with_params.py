"""Illustrate how to create a decorator with parameters."""

from collections.abc import Callable
from typing import Any


def monitor(
    label: str | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Monitor function calls with a custom label."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorate the function to add monitoring."""

        def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
            """Wrap the function to monitor its execution."""
            if label:
                print(f">>> {label}: {func.__name__!r} invoked: {args=};{kwargs=}.")
            else:
                print(f">>> {func.__name__!r} invoked: {args=};{kwargs=}.")
            result = func(*args, **kwargs)
            if label:
                print(f">>> {label}: {func.__name__!r} returned {result!r}.")
            else:
                print(f">>> {func.__name__!r} returned {result!r}.")
            return result

        return wrapper

    return decorator


# Note that because it accepts arguments, you need to use ()
@monitor()
def say_hello() -> None:
    """Say hello."""
    print("Hello!")


@monitor("custom msg")
def get_greeting(name: str) -> str:
    """Return a personalized greeting."""
    return f"Hello, {name}!"


def main() -> None:
    """Application entry point."""
    say_hello()
    print(get_greeting("Alice"))


if __name__ == "__main__":
    main()
