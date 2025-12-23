"""Consumes the mymath module via 'from module import *'."""

from mymath import *  # noqa: F403


def main() -> None:
    """Application entry point."""
    radius = 5
    circle_area = area(radius)  # noqa: F405
    print(f"The area of a circle with radius {radius} is {circle_area}")

    # pi is not imported with the wildcard import
    try:
        print(f"pi as defined in mymath: {pi}")  # ty:ignore[undefined-variable]  # noqa: F405  # ty:ignore[unresolved-reference, ignore-comment-unknown-rule]
    except NameError as e:
        print(f"Error: {e}")

    # same thing for the _version variable
    try:
        print(f"_version as defined in mymath: {_version}")  # ty:ignore[undefined-variable]  # noqa: F405  # ty:ignore[unresolved-reference, ignore-comment-unknown-rule]
    except NameError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
