"""Calculator abstract interface."""

from abc import ABC, abstractmethod


class Calculator(ABC):
    """Abstract interface for a calculator."""

    @abstractmethod
    def put_value(self, value: float) -> None:
        """Put a number into the internal stack."""

    @abstractmethod
    def get_value(self) -> float:
        """Pop a number from the internal stack."""

    @abstractmethod
    def peek_value(self) -> float:
        """Peeks the number at the top of the stack without removing it."""

    @abstractmethod
    def clear(self) -> None:
        """Remove all the numbers from the internal stack."""

    @abstractmethod
    def divide(self) -> float:
        """Perform a division."""

    @abstractmethod
    def multiply(self) -> float:
        """Perform a multiplication."""
