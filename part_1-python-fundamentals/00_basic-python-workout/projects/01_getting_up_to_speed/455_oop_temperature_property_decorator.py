"""Using property decorator for a simple Temperature class."""


class Temperature:
    """Class representing temperature in Celsius."""

    def __init__(self, fahrenheit: float) -> None:
        """Initialize the temperature with a Fahrenheit value."""
        self._temp_fahrenheit = fahrenheit

    @property
    def temp(self) -> float:
        """Get the temperature in Celsius."""
        return (self._temp_fahrenheit - 32) * 5 / 9

    @temp.setter
    def temp(self, value: float) -> None:
        """Set the temperature in Celsius."""
        self._temp_fahrenheit = (value * 9 / 5) + 32

    def __repr__(self) -> str:
        """Return a developer-friendly string representation of the temperature."""
        return f"Temperature({self.temp:.2f} °C)"


def main() -> None:
    """Application entry point."""
    temp = Temperature(100)
    print(temp)  # Should print Temperature(37.78 °C)
    temp.temp = 100
    print(temp)  # Should print Temperature(100.00 °C)


if __name__ == "__main__":
    main()
