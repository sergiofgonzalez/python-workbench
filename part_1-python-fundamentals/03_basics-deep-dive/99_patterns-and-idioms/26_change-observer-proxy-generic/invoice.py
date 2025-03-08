"""Invoice object definition."""


class Invoice:
    """Invoice class."""

    def __init__(self, subtotal: float, discount: float, tax: float) -> None:
        """Invoice instance initialization."""
        self.subtotal = subtotal
        self.discount = discount
        self.tax = tax

    def calculate_total(self) -> float:
        """Calculate the total of the invoice."""
        return self.subtotal - self.discount + self.tax
