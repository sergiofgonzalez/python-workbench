"""Illustrate the use of or/and expressions for defaults and short-circuiting."""


def main() -> None:
    """Application entry point."""
    # Using or to provide a default value
    name = input("Enter your name (can be empty): ") or "stranger"
    print(f"Hello, {name}!")

    # Using and for short-circuiting
    x = 0
    y = 5
    print(f"{x=}; {y=}; {x and y=}")
    print(x if not x else y)

    x = True
    y = False
    print(f"{x=}; {y=}; {x and y=}")
    print(x if not x else y)

    x = "some"
    y = ""
    print(f"{x=}; {y=}; {x and y=}")
    print(x if not x else y)



if __name__ == "__main__":
    main()
