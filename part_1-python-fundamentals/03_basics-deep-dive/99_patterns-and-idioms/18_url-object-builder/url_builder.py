"""Builder pattern for the URL object."""

from url import URL


class URLBuilder:
    """Implementation of the Builder pattern for a URL oject."""

    def __init__(self) -> None:
        """Object initializer for the URLBuilder object."""
        self.protocol = ""
        self.username = None
        self.password = None
        self.hostname = ""
        self.port = None
        self.pathname = None
        self.search = None
        self.hash_part = None

    def set_protocol(self, protocol: str) -> "URLBuilder":
        """Configure the protocol of the URL."""
        self.protocol = protocol
        return self

    def set_authentication(self, username: str, password: str) -> "URLBuilder":
        """Configure the credentials part of the URL."""
        self.username = username
        self.password = password
        return self

    def set_hostname(self, hostname: str, port: int | None = None) -> "URLBuilder":
        """Configure the hostname and port part of the URL."""
        self.hostname = hostname
        self.port = port
        return self

    def set_pathname(self, pathname: str) -> "URLBuilder":
        """Configure the pathname of the URL."""
        self.pathname = pathname
        return self

    def set_search(self, search: str) -> "URLBuilder":
        """Configure the search part of the URL."""
        self.search = search
        return self

    def set_hash(self, hash_part: str) -> "URLBuilder":
        """Configure the hash part of the URL."""
        self.hash_part = hash_part
        return self

    def build(self) -> URL:
        """Return a properly configured URL object instance."""
        if not self.protocol:
            msg = "protocol is required"
            raise ValueError(msg)
        if (self.username and not self.password) or (
            not self.username and self.password
        ):
            msg = "when using credentials both username and password are required"
            raise ValueError(msg)
        if self.port and not isinstance(self.port, int):
            msg = "when specified port must be an int"
            raise TypeError(msg)
        return URL(
            protocol=self.protocol,
            username=self.username,
            password=self.password,
            hostname=self.hostname,
            port=self.port,
            pathname=self.pathname,
            search=self.search,
            hash_part=self.hash_part,
        )
