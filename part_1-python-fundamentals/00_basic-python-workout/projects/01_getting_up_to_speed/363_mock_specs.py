"""Illustrates the concept of Mock specs."""
from unittest.mock import Mock

cldr_mock = Mock(spec=["is_weekday", "get_holidays"])

def main() -> None:
    """Application entry point."""
    print(cldr_mock.is_weekday())
    print(cldr_mock.get_holidays())
    try:
        print(cldr_mock.non_existent_method())
    except AttributeError as e:
        print(f"Caught an AttributeError as expected: {e}")

if __name__ == "__main__":
    main()
