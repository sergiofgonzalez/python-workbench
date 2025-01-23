"""ColorConsole class."""

from enum import Enum, auto
from typing import override


class ColorConsole:
    """Class to print messages in the terminal."""

    def log(self, msg: str) -> None:
        """Print the message in the terminal."""
        print(msg)


class RedConsole(ColorConsole):
    """Class to print messages in red in the terminal."""

    @override
    def log(self, msg: str) -> None:
        """Print the message in the terminal."""
        print(f"\x1b[31m{msg}\x1b[0m")


class BlueConsole(ColorConsole):
    """Class to print messages in blue in the terminal."""

    @override
    def log(self, msg: str) -> None:
        """Print the message in the terminal."""
        print(f"\x1b[34m{msg}\x1b[0m")


class GreenConsole(ColorConsole):
    """Class to print messages in green in the terminal."""

    @override
    def log(self, msg: str) -> None:
        """Print the message in the terminal."""
        print(f"\x1b[32m{msg}\x1b[0m")


class Color(Enum):
    """Supported colors for the console."""

    RED = auto()
    GREEN = auto()
    BLUE = auto()


def get_color_console(color: Color) -> None:
    """Return the concrete ColorConsole class to print messages in that color."""
    consoles = {
        Color.RED: RedConsole(),
        Color.GREEN: GreenConsole(),
        Color.BLUE: BlueConsole(),
    }
    return consoles[color]
