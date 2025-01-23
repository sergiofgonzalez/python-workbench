"""Simple HTTP server that displays the info it receives in the request."""

import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import override
from urllib.parse import parse_qs, urlparse


class CustomRequestHandler(BaseHTTPRequestHandler):
    """Incoming request handler."""

    def print_req_info(self) -> None:
        """Print request information."""
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode()

        print(f"HTTP method: {self.command}")
        print(f"Full URL: {self.path}")
        print(f"Path part: {parsed_path.path}")
        print(f"Search part: {parsed_path.query}")
        print(f"Query parameters: {query_params}")
        print(f"HTTP headers: {self.headers.items()}")
        print(f"Body: {body if body else '(empty)'}")

    @override
    def do_GET(self) -> None:
        self.print_req_info()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK\n")

    @override
    def do_PUT(self) -> None:
        self.print_req_info()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK\n")

    @override
    def log_message(self, format: str, *args: str) -> None:
        """Disable logging."""

    # @override
    # def do_PUT(self) -> None:
    #     self.send_response(201)
    #     self.send_header("Content-Type", "text/plain")
    #     self.end_headers()
    #     self.wfile.write(b"OK\n")
    #     logger.info(
    #         "request for {filename}successfully processed",
    #         filename=self.headers["x-filename"],
    #     )


def run_server(port: int | None = 8080) -> None:
    """Run a basic HTTP server that prints the information about the req it receives."""
    server_address = ("", port)
    httpd = HTTPServer(server_address, CustomRequestHandler)
    print(f"Server listening in port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) == 2:  # noqa: PLR2004
        try:
            port = int(sys.argv[1])
        except TypeError as e:
            print(f"PORT must be an int: {e}")
            sys.exit(1)
        run_server(port)
    else:
        run_server()
