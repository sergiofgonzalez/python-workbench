"""Exercise on scopes (local, nonlocal, global)."""

g_var = 0
nl_var = 0


def outer_fn() -> None:  # noqa: D103
    nl_var = 2
    assert g_var == 0
    assert nl_var == 2  # noqa: PLR2004

    def inner_fn() -> None:
        global g_var  # noqa: PLW0603
        nonlocal nl_var
        g_var = 1
        nl_var = 4
        assert g_var == 1
        assert nl_var == 4  # noqa: PLR2004

    inner_fn()
    assert g_var == 1
    assert nl_var == 4  # noqa: PLR2004


def main() -> None:
    """Application entry point."""
    outer_fn()
    assert g_var == 1
    assert nl_var == 0
    print("=== All assertions passed! ===")


if __name__ == "__main__":
    main()
