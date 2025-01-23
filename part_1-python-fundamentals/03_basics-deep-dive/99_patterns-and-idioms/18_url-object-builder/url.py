"""URL object."""

from io import StringIO


class URL:
    """Object that represents a URL."""

    def __init__(  # noqa: PLR0913
        self,
        protocol: str,
        username: str | None,
        password: str | None,
        hostname: str,
        port: int | None,
        pathname: str | None,
        search: str | None,
        hash_part: str | None,
    ) -> None:
        """Initialize a URL instance."""
        self.protocol = protocol
        self.username = username
        self.password = password
        self.hostname = hostname
        self.port = port
        self.pathname = pathname
        self.search = search
        self.hash_part = hash_part
        self._validate()

    def _validate(self) -> None:
        """Validate the URL is correct."""
        if not self.protocol or not self.hostname:
            msg = "A URL must at least specify a protocol and a hostname"
            raise ValueError(msg)

    def __str__(self) -> str:
        """Return the representation of the URL."""
        url = StringIO()
        url.write(f"{self.protocol}://")
        if self.username and self.password:
            url.write(f"{self.username}:{self.password}@")
        url.write(self.hostname)
        if self.port:
            url.write(f":{self.port}")
        if self.pathname:
            url.write(self.pathname)
        if self.search:
            url.write(f"?{self.search}")
        if self.hash_part:
            url.write(f"#{self.hash_part}")
        return url.getvalue()
