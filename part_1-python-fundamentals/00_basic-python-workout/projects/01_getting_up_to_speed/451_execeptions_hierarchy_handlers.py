"""Illustrates the role of exception hierarchy in exception handlers."""


def main() -> None:
    """Application entry point."""
    #     ├── LookupError
    #         ├── IndexError
    #         └── KeyError

    # Because IndexError is a subclass of LookupError, the LookupError
    # handler will catch the IndexError exception only.
    try:
        raise IndexError("An index error occurred")  # noqa: EM101, TRY003, TRY301
    except LookupError as le:
        print(f"Caught LookupError: {le}")
    except IndexError as ie:
        print(f"Caught IndexError: {ie}")
    except KeyError as ke:
        print(f"Caught KeyError: {ke}")

    # If you want to be able to handle IndexError separately,
    # you need to place its handler before the LookupError handler.
    try:
        raise IndexError("An index error occurred")  # noqa: EM101, TRY003, TRY301
    except IndexError as ie:
        print(f"Caught IndexError: {ie}")
    except KeyError as ke:
        print(f"Caught KeyError: {ke}")
    except LookupError as le:
        print(f"Caught LookupError: {le}")

    # Note that exception groups won't help either
    try:
        raise ExceptionGroup(  # noqa: TRY003
            "Multiple errors occurred",  # noqa: EM101
            [
                IndexError("Index error in group"),
                KeyError("Key error in group"),
            ],
        )
    except* LookupError as le:
        print(f"Caught LookupError(s): {[str(e) for e in le.exceptions]}")
    except* IndexError as ie:
        print(f"Caught IndexError(s): {[str(e) for e in ie.exceptions]}")
    except* KeyError as ke:
        print(f"Caught KeyError(s): {[str(e) for e in ke.exceptions]}")

if __name__ == "__main__":
    main()
