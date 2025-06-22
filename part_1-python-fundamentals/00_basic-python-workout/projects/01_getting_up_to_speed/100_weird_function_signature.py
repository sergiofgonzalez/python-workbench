"""Illustrate the use of * in function signatures."""


def weird(
    param1: str,
    param2: str,
    *,
    prefix: str | None = None,
    **kwargs: str,
) -> None:
    """Illustrate a function with a weird signature.

    Args:
        param1 (int): An integer parameter.
        param2 (str): A string parameter.
        prefix: An optional prefix for the output.
        **kwargs: Additional keyword arguments.

    Returns:
        None

    """
    print(f"{param1=}, {param2=}, {prefix=}, {kwargs=}")


def normal(
    param1: str,
    param2: str,
    prefix: str | None = None,
    **kwargs: str,
) -> None:
    """Illustrate a function with a normal signature.

    Args:
        param1 (int): An integer parameter.
        param2 (str): A string parameter.
        prefix: An optional prefix for the output.
        **kwargs: Additional keyword arguments.

    Returns:
        None

    """
    print(f"{param1=}, {param2=}, {prefix=}, {kwargs=}")


def main() -> None:
    """Application entry point."""
    weird("p1", "p2")
    weird(param2="p2", param1="p1")
    # weird("p1", "p2", "other") # Takes 2 positional arguments, not 3.  # noqa: ERA001
    weird("p1", "p2", other="some other value")
    weird("p1", "p2", other="some other value", some="some")
    weird("p1", "p2", prefix="yay")
    weird("p1", "p2", prefix="yay", some="some", other="other", value="value")
    print("=" * 20)

    normal("p1", "p2")
    normal(param2="p2", param1="p1")
    normal("p1", "p2", "other")  # Third parameter is taken as prefix.
    normal("p1", "p2", other="some other value")
    normal("p1", "p2", prefix="yay")
    normal("p1", "p2", prefix="yay", some="some", other="other", value="value")


if __name__ == "__main__":
    main()
