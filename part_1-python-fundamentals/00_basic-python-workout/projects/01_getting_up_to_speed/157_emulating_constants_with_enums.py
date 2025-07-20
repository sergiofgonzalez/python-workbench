"""Illustrate how to emulate constants with enums."""

from enum import Enum


class Constants(Enum):
    """An enumeration for different constants."""

    WIDTH = 1024
    HEIGHT = 768


# Using a constant directly
WIDTH = 1024  # This is a simple constant, not an enum member


def main() -> None:
    """Application entry point."""
    print("Constants.WIDTH:", Constants.WIDTH)
    print("Constants.HEIGHT:", Constants.HEIGHT)

    # Accessing the value using the '.' syntax
    print(f"Width: {Constants.WIDTH.value}")
    print(f"Height: {Constants.HEIGHT.value}")

    # You cannot change the value of an enum member
    try:
        Constants.WIDTH = 800  # type: ignore  # noqa: PGH003
    except AttributeError as e:
        print(f"Error: {e}")

    # DX is so-so, as you need to use the '.' notation to get the value
    # but the alternative is to rely on nomenclature, which is not as clear

    print("Width constant (good DX, but it's not a constant):", WIDTH)


if __name__ == "__main__":
    main()
