"""Illustrate how to use Mock autospec."""

from unittest.mock import create_autospec, patch

from lib import cldr


def main() -> None:
    """Application entry point."""
    cldr_mock = create_autospec(cldr)
    cldr_mock.is_weekday.return_value = False
    print("Is weekday (mocked):", cldr_mock.is_weekday())
    print("Is weekday (real):", cldr.is_weekday())

    with patch.object(cldr, "is_weekday", autospec=True) as mock_is_weekday:
        mock_is_weekday.return_value = False
        print("Is weekday (patched):", cldr.is_weekday())

    with patch("lib.cldr", autospec=True) as mock_cldr:
        print("mock_cldr.is_weekday (patched):", mock_cldr.is_weekday())
        print("mock_cldr.get_holidays (patched):", mock_cldr.get_holidays())
        try:
            print(
                "mock_cldr.non_existent_method (patched):",
                mock_cldr.non_existent_method(),
            )
        except AttributeError as e:
            print(f"Caught an AttributeError as expected: {e}")


if __name__ == "__main__":
    main()
