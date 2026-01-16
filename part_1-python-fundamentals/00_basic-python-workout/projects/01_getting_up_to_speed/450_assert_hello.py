"""Illustrates the basics of assert."""


def main() -> None:
    """Application entry point."""
    assert True, "This should not raise an AssertionError"
    print("Assertion passed: True is truthy")

    try:
        assert False, "This should raise an AssertionError"  # noqa: B011, PT015
    except AssertionError as e:
        print(f"Caught AssertionError: {e}")


if __name__ == "__main__":
    main()
