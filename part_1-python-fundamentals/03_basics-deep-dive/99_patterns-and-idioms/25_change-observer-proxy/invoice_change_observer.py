"""A concrete implementation of the Change Observer Pattern for an Invoice object."""

from collections.abc import Callable
from typing import Any

from invoice import Invoice


class ObservableInvoice(Invoice):
    """Implementation of the Change Observer Pattern for an Invoice object."""

    def __init__(
        self,
        target_invoice: Invoice,
        observer_fn: Callable[[str, Any, Any], Any],
    ) -> None:
        """Initialize an ObservableInvoice object."""
        self._target_invoice = target_invoice
        self._observer_fn = observer_fn

    @property
    def subtotal(self) -> float:
        """Return the underlying subtotal attribute value."""
        return self._target_invoice.subtotal

    @subtotal.setter
    def subtotal(self, value: float) -> None:
        """Set the underlying subtotal if different from prev value."""
        prev_value = self._target_invoice.subtotal
        if value != prev_value:
            self._target_invoice.subtotal = value
            self._observer_fn("subtotal", prev_value, value)

    @property
    def discount(self) -> float:
        """Return the underlying discount attribute value."""
        return self._target_invoice.discount

    @discount.setter
    def discount(self, value: float) -> None:
        """Set the underlying discount if different from prev value."""
        prev_value = self._target_invoice.discount
        if value != prev_value:
            self._target_invoice.discount = value
            self._observer_fn("discount", prev_value, value)

    @property
    def tax(self) -> float:
        """Return the underlying tax attribute value."""
        return self._target_invoice.discount

    @tax.setter
    def tax(self, value: float) -> None:
        """Set the underlying tax if different from prev value."""
        prev_value = self._target_invoice.tax
        if value != prev_value:
            self._target_invoice.tax = value
            self._observer_fn("tax", prev_value, value)

    def calculate_total(self) -> float:
        """Return the calculate_total of the underlying invoice."""
        return self._target_invoice.calculate_total()
