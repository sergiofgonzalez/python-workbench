"""Illustrates the basics of exception groups."""


def main() -> None:
    """Application entry point."""
    try:
        raise ExceptionGroup(  # noqa: TRY003
            "Multiple errors occurred",  # noqa: EM101
            [
                ValueError("Invalid value"),
                TypeError("Type mismatch"),
                KeyError("Missing key"),
                ValueError("Another invalid value"),
            ],
        )
    except* ValueError as ve:
        print(f"Caught ValueError(s): {[str(e) for e in ve.exceptions]}")
    except* TypeError as te:
        print(f"Caught TypeError(s): {[str(e) for e in te.exceptions]}")
    except* KeyError as ke:
        print(f"Caught KeyError(s): {[str(e) for e in ke.exceptions]}")


if __name__ == "__main__":
    main()
