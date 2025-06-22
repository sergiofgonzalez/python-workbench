"""Illustrates the basic use of lists and unpacking in Python."""


def main() -> None:
    """Application entry point."""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

    # First and 4th month
    first = months[0]
    fourth = months[3]
    print(f"First month: {months[0]}, Fourth month: {months[3]}")
    assert first == "Jan"
    assert fourth == "Apr"

    # Month before last
    print(f"Month before last: {months[-2]}")
    assert months[-2] == "May"

    # Unpacking the list
    jan, feb, mar, apr, may, jun = months
    print(f"Unpacked months: {jan}, {feb}, {mar}, {apr}, {may}, {jun}")
    assert (jan, feb, mar, apr, may, jun) == ("Jan", "Feb", "Mar", "Apr", "May", "Jun")


if __name__ == "__main__":
    main()
