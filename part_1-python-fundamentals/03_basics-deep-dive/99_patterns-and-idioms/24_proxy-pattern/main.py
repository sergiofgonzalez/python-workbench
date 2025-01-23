"""Illustrates the ideal way to implement the Proxy design pattern in Python."""

from abc import ABC, abstractmethod


class Subject(ABC):
    """
    The Subject interface declares common operations for both RealSubject and the
    Proxy. As long as the client works with RealSubject using this interface, you'll
    be able to pass it a proxy instead of a real subject.
    """

    @abstractmethod
    def request(self) -> None:
        """Operation we want to control from the proxy."""


class RealSubject(Subject):
    """
    The RealSubject object that we want to proxy.
    """

    def request(self) -> None:
        """Operation."""
        print("RealSubject.request(): handling the request.")


class Proxy(Subject):
    """
    The Proxy has an interface identical to the RealSubject.
    """

    def __init__(self, real_subject: RealSubject) -> None:
        """Initialize an instance of the proxy."""
        self._real_subject = real_subject

    def request(self) -> None:
        """
        Proxied method implementation which implement behavior that differ
        the one in the RealSubject.
        """
        if self.check_access():
            self._real_subject.request()
            self.log_access()

    def check_access(self) -> bool:
        """Return True for all request."""
        return True

    def log_access(self) -> None:
        """Log the request."""
        print("Proxy: Logging the request.")


def main() -> None:
    """Application entry point."""
    real_subject = RealSubject()
    real_subject.request()

    # Using the proxy
    proxy = Proxy(real_subject)
    proxy.request()


if __name__ == "__main__":
    main()
