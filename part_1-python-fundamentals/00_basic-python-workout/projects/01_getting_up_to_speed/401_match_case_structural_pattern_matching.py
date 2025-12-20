"""match-case structural pattern matching example."""


def main() -> None:
    """Application entry point."""
    x = [1, 2, 3]
    match x:
        case "A":
            print("Matched string A")
        case str() as s:
            print(f"Matched a string: {s}")
        case 0:
            print("Matched zero")
        case 1 | 2 | 3 as n:
            print(f"Matched one, two, or three: {n}")
        case int() as n if n > 0:
            print(f"Matched a positive integer other than 1, 2, 3: {n}")
        case int():
            print(f"Matched a non-positive integer: {n}")
        case _ as m:
            print(f"Neither string nor integer was matched: {m}")


if __name__ == "__main__":
    main()
