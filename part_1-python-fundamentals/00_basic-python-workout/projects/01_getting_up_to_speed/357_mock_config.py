"""A practical example of how to configure a mock."""

from unittest.mock import Mock


def say_hello(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"


def main() -> None:
    """Application entry point."""
    # Configure a mock with a name
    mock1 = Mock(name="MyMock1")
    print(mock1())
    print(f"{mock1.name=}")
    print("=" * 40)

    # Configure a mock with a name and a return value
    mock2 = Mock(name="MyMock2", return_value=42)
    print(mock2())
    print(f"{mock2.name=}")
    print(mock2.return_value)
    print("=" * 40)

    # Configure a mock with a name, a return value, and side effects
    mock3 = Mock(name="MyMock3", return_value="Hi", side_effect=lambda: "Hello!")
    print(mock3())
    print(f"{mock3.name=}")
    print(mock3.return_value)
    print("=" * 40)

    # A mock can also be configured with a spcecific function
    holidays = {
        "2025-01-01": "New Year's Day",
        "2025-07-04": "Independence Day",
        "2025-12-25": "Christmas Day",
    }
    mock4 = Mock(**{"name": "MyMock4", "json.return_value": holidays})
    print(f"{mock4.name=}")
    print(f"{mock4.json()=}")
    print("=" * 40)


if __name__ == "__main__":
    main()
