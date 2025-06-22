"""Using isinstance with built-in types."""


def main() -> None:
    """Application entry point."""
    s = "foobar"
    t = (1, "a")
    d = {"name": "jason", "age": 35}

    print(f"{isinstance(s, str)=}")
    print(f"{isinstance(t, tuple)=}")
    print(f"{isinstance(d, dict)=}")


if __name__ == "__main__":
    main()
