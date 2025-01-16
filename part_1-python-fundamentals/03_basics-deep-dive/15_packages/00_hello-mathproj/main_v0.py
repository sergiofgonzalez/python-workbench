"""Illustrate how to create and work with packages in Python."""

import mathproj


def main() -> None:
    """Application entry point."""
    print("Hello from 00-hello-mathproj!")

    # You can refer to the variable defined in mathproj's __init__.py
    print(mathproj.version)

    # subpackages are not loaded when loading the top-level package
    try:
        mathproj.comp.numeric.n1.g()
    except AttributeError as e:
        print(f"Oops! {e} ({type(e)})")



if __name__ == "__main__":
    main()
