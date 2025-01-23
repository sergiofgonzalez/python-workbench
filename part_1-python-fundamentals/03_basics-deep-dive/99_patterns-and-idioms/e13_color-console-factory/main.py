"""Illustrate how to use the ColorConsole class."""

from color_console import Color, get_color_console


def main() -> None:
    """Application entry point."""
    green = get_color_console(Color.GREEN)
    red = get_color_console(Color.RED)
    blue = get_color_console(Color.BLUE)
    green.log("Hello, world!")
    red.log("Hello, world!")
    blue.log("Hello, world!")


if __name__ == "__main__":
    main()
