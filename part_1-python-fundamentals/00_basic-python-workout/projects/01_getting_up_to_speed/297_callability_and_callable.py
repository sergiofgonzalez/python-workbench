"""Examples on callability and the callable keyword."""

from collections.abc import Callable


class Task:
    """A simple callable class representing a task."""

    def __init__(self, title: str, description: str, urgency: int) -> None:
        """Initialize the Task."""
        self.title = title
        self.description = description
        self.urgency = urgency

    def __call__(self, *args: object, **kwargs: object) -> object:
        """Make the instance callable."""
        print(f"Received invocation: {args}, {kwargs}")
        return repr(self)

    def __repr__(self) -> str:
        """Developer-friendly string representation of the Task."""
        attrs = ", ".join([f"{k} = {self.__dict__[k]!r}" for k in self.__dict__])
        return f"Task({attrs})"


def doubler(x: int) -> int:
    """Return double the input value."""
    return x * 2


def apply(f: Callable, *args: object) -> object:
    """Apply the callable f to the provided arguments."""
    return f(*args)


def main() -> None:
    """Application entry point."""
    print(callable(doubler))
    assert callable(doubler)

    # using the apply function to call doubler
    result = apply(doubler, 5)
    print(f"Result of applying doubler to 5: {result}")
    assert result == 10  # noqa: PLR2004

    # using the apply function with a custom class
    result = apply(
        Task,
        "Write Code",
        "Write code examples for callability in Python.",
        1,
    )
    print(f"Result of applying Task constructor: {result}")
    assert isinstance(result, Task)
    assert result.title == "Write Code"
    assert result.description == "Write code examples for callability in Python."
    assert result.urgency == 1

    # we can also send the parameters as a tuple
    params = ("Review Code", "Review code examples for callability in Python.", 2)
    result = apply(Task, *params)
    print(f"Result of applying Task constructor with params tuple: {result}")
    assert isinstance(result, Task)
    assert result.title == "Review Code"
    assert result.description == "Review code examples for callability in Python."
    assert result.urgency == 2  # noqa: PLR2004

    # Trying to spot the type of a callable
    print(f"Type of doubler: {type(doubler)}")
    print(f"Type of Task: {type(Task)}")
    print(f"Type of sum(): {type(sum)}")
    print("=" * 20)
    # Now without type
    print(f"Type of doubler: {doubler}")
    print(f"Type of Task: {Task}")
    print(f"Type of sum(): {sum}")

    # Checking that the Task instances are callable
    task = Task("Gym", "Burn some calories", 5)
    print(task("hello", "world", param1="uno"))


if __name__ == "__main__":
    main()
