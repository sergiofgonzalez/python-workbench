"""Main program of the application."""

from collections.abc import Callable

from invoice import Invoice
from observable import Observable


def print_change(property_name: str, prev_value: float, value: float) -> None:
    """Observer function that simply prints the change in the terminal."""
    print(f"Property {property_name!r} changed: {prev_value} => {value}")


def main() -> None:
    """Application entry point."""
    invoice = Invoice(subtotal=100, discount=10, tax=20)
    total = invoice.calculate_total()
    print(f"Starting total: {total}")

    # Now the change observer piece
    print("=" * 80)
    observable_invoice = Observable(invoice, observer=print_change)
    observable_invoice.subtotal = 200
    observable_invoice.discount = 20
    observable_invoice.tax = 15
    print(f"Final total: {observable_invoice.calculate_total()}")

    # You can make it fancier with a fn that returns a closure on the invoice
    # which we use as the observer function
    # print("=" * 80)
    # another_observable_invoice = ObservableInvoice(
    #     invoice,
    #     observer_fn=get_observer_fn(invoice),
    # )
    # another_observable_invoice.subtotal = 210
    # another_observable_invoice.discount = 25
    # another_observable_invoice.tax = 20


if __name__ == "__main__":
    main()
