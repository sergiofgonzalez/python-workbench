"""Consumes the mymath module via 'import module'."""

import mymath


def main() -> None:
    """Application entry point."""
    print(f"Module mymath contents: {dir(mymath)}")

    # the area function is imported in mymath/__init__.py
    radius = 5
    circle_area = mymath.area(radius)
    print(f"The area of a circle with radius {radius} is {circle_area}")

    # pi is not exported and therefore not accessible directly from mymath
    try:
        print(f"pi as defined in mymath: {mymath.pi}")  # ty:ignore[unresolved-attribute]
    except AttributeError as e:
        print(f"Error: {e}")

    # but it can be accessed via the submodule
    print(f"pi as defined in mymath.my_math_thingies: {mymath.my_math_thingies.pi}")

    # same thing for the _version variable
    try:
        print(f"_version as defined in mymath: {mymath._version}")  # ty:ignore[unresolved-attribute]  # noqa: SLF001
    except AttributeError as e:
        print(f"Error: {e}")
    print(
        f"_version as defined in mymath.my_math_thingies: {mymath.my_math_thingies._version}",  # noqa: E501, SLF001
    )


if __name__ == "__main__":
    main()
