"""Illustrates the full syntax of an exception block."""


def main() -> None:
    """Application entry point."""
    try:
        print("In try block")
    except ZeroDivisionError as e:
        print(f"Caught a ZeroDivisionError exception: {e}")
    except ValueError as e:
        print(f"Caught a ValueError exception: {e}")
    except (TypeError, IndexError) as e1:
        print(f"Caught a TypeError or IndexError exception: {e1}")
    except:  # noqa: E722
        print("Caught an unexpected exception.")
    else:
        print("No exceptions or return in body occurred.")
    finally:
        print("Executing finally block.")


if __name__ == "__main__":
    main()
