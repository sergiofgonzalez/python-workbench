"""Illustrate how to create and work with packages in Python."""

import mathproj.comp.numeric.n1


def main() -> None:
    """Application entry point."""
    print("Hello from 00-hello-mathproj!")

    # You can refer to the variable defined in mathproj's __init__.py when
    # loading the subpackage
    print(mathproj.version)

    # Now we can invoke g()
    try:
        g()  # noqa: F821
    except Exception as e:  # noqa: BLE001
        print(f"Oops! {e} ({type(e)})")

    # but it has to be qualified
    try:
        mathproj.comp.numeric.n1.g()
    except Exception as e:  # noqa: BLE001
        print(f"Oops! {e} ({type(e)})")


if __name__ == "__main__":
    main()
