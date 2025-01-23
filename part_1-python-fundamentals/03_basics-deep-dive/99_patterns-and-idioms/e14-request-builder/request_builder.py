"""Builder pattern for sending an HTTP request with the requests library."""

from enum import Enum, auto

import requests


class HttpMethod(Enum):
    """Supported HTTP methods."""

    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    PATCH = auto()
    HEAD = auto()
    OPTIONS = auto()


class RequestBuilder:
    """Builder pattern for the requests.x() functions."""

    def __init__(self) -> None:
        """Initialize a RequestBuilder instance."""
        self.method = None
        self.url = None
        self.query_params = {}
        self.headers = {}
        self.body = None

    def set_method(self, method: HttpMethod) -> "RequestBuilder":
        """Set the HTTP method."""
        self.method = method
        return self

    def set_url(self, url: str) -> "RequestBuilder":
        """Set the URL of the request."""
        self.url = url
        return self

    def add_query_param(self, param_name: str, param_value: str) -> "RequestBuilder":
        """Add or update a query parameter of the request."""
        self.query_params[param_name] = param_value
        return self

    def add_header(self, header_name: str, header_value: str) -> "RequestBuilder":
        """Add or update a query parameter of the request."""
        self.headers[header_name.lower()] = header_value
        return self

    def set_body(self, body: str) -> "RequestBuilder":
        """Set the body of the request."""
        self.body = body
        return self

    def invoke(self) -> requests.Response:
        """Return the result of the invocation."""
        if not self.url:
            msg = "URL was not specified"
            raise ValueError(msg)
        if not self.method:
            msg = "HTTP method was not specified"
            raise ValueError(msg)
        if self.body and "Content-Length".lower() not in self.headers:
            self.headers["Content-Length"] = str(len(self.body))

        kwargs = {
            "url": self.url,
            "params": self.query_params,
            "headers": self.headers,
            "data": self.body,
        }

        req_fns = {
            HttpMethod.GET: requests.get,
            HttpMethod.POST: requests.post,
            HttpMethod.PUT: requests.put,
            HttpMethod.DELETE: requests.delete,
            HttpMethod.PATCH: requests.patch,
            HttpMethod.OPTIONS: requests.options,
            HttpMethod.HEAD: requests.head,
        }

        return req_fns[self.method](**kwargs)
