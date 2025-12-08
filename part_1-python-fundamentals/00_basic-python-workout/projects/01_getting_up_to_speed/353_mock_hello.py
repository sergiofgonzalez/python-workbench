"""The simplest mock example."""

from unittest.mock import Mock


def main() -> None:
    """Application entry point."""
    mock = Mock()
    print(mock, type(mock).__name__)

    # You mock the json module
    json = mock
    print(json, type(mock).__name__)
    print(json.dumps({"hello": "world"}), type(mock).__name__)

    # Or access attributes that don't exist
    print(json.foo, type(mock).__name__)

    # and invoked methods return a mock, so you can chain calls
    print(json.loads("{'hello': 'world'}").get("hello"), type(mock).__name__)


if __name__ == "__main__":
    main()
