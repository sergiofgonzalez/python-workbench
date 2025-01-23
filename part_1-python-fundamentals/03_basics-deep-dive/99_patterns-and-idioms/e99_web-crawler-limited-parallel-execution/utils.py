"""Web scraping utils."""

import re
import urllib.parse
from pathlib import Path

from slugify import slugify


def url_to_filename(url: str) -> Path:
    """Map an URL to a filename returned as a Path object."""
    parsed_url = urllib.parse.urlparse(url)
    path_components = parsed_url.path.split("/")
    components = [
        slugify(component) for component in path_components if component != ""
    ]
    url_path = "/".join(components)
    filename = Path(parsed_url.hostname, url_path)
    if not re.match(r"htm", filename.suffix):
        filename = filename.with_suffix(".html")
    return filename
