"""HTTP server that uncompresses and saves a gzipped file received in the request."""

import gzip
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import override

import typer
from loguru import logger


class CustomRequestHandler(BaseHTTPRequestHandler):
    """Incoming request handler."""

    @override
    def do_PUT(self) -> None:
        process_file(self)
        self.send_response(201)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK\n")
        logger.info(
            "request for {filename}successfully processed",
            filename=self.headers["x-filename"],
        )


def process_file(request: CustomRequestHandler) -> None:
    """Process the file coming in the request."""
    filename = Path(request.headers["x-filename"]).name
    dest_filename = Path("received_files", filename)
    logger.info(
        "request received for file {} which will be saved in {}",
        filename,
        dest_filename,
    )
    remaining_bytes = int(request.headers["Content-Length"])
    logger.info("reported file {} size: {} bytes", filename, remaining_bytes)
    dest_filename.parent.mkdir(parents=True, exist_ok=True)
    while gzipped_chunk := request.rfile.read(min(remaining_bytes, 256)):
        chunk = gzip.decompress(gzipped_chunk)
        print(chunk)
    logger.info("{} saved", filename)


def run_server(port: int | None = 8000) -> None:
    """Run an HTTP server that gunzips and saves a gz file received in the request."""
    server_address = ("", port)
    httpd = HTTPServer(server_address, CustomRequestHandler)
    logger.info("server running on port {}", port)
    httpd.serve_forever()


if __name__ == "__main__":
    typer.run(run_server)
