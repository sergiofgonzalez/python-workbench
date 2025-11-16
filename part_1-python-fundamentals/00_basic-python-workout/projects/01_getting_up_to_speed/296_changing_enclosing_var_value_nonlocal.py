"""Illustrate how to change the value of an enclosing variable using nonlocal."""


def change_text(*, using_nonlocal: bool) -> str:
    """Change the text variable in the enclosing scope."""
    text = "N/A"

    def inner_fun0() -> None:
        # The following line would create a new local variable instead of
        # modifying the enclosing one
        text = "no nonlocal used"  # noqa: F841

    def inner_fun1() -> None:
        # Here we announce that we want to use the enclosing scope's variable
        nonlocal text
        text = "nonlocal used"

    inner_fun1() if using_nonlocal else inner_fun0()
    return text


def main() -> None:
    """Application entry point."""
    print(change_text(using_nonlocal=False))
    print(change_text(using_nonlocal=True))


if __name__ == "__main__":
    main()
