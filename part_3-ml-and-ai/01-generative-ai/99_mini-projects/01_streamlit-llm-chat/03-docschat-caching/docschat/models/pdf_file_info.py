"""
PDF file model for the LLM DocBot app.
"""

from collections import namedtuple

PdfFileInfo = namedtuple("PdfFileInfo", ["friendly_name", "temp_path", "hash"])
