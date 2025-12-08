"""Illustrates some assertion and inspection methods available in Mock."""

from unittest.mock import Mock


def main() -> None:
    """Application entry point."""
    json = Mock()

    # Call it
    json.loads('{"hello": "world"}')

    # Now use assertions
    json.loads.assert_called()
    json.loads.assert_called_once()
    json.loads.assert_called_with('{"hello": "world"}')

    # if an assertion fails, an AssertionError is raised
    try:
        json.loads.assert_called_with('{"goodbye": "world"}')
    except AssertionError as ex:
        print(f"AssertionError: {ex}")


    # you can also inspect call args directly
    print(f"{json.loads.call_count=}")
    print(f"{json.loads.call_args=}")
    print(f"{json.loads.call_args_list=}")
    print(f"{json.loads.method_calls=}")

if __name__ == "__main__":
    main()
