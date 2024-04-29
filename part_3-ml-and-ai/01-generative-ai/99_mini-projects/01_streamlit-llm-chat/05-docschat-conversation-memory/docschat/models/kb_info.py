"""
PDF file model for the LLM DocBot app.
"""

from collections import namedtuple
from typing import Dict

PdfFileInfo = namedtuple("PdfFileInfo", ["friendly_name", "temp_path", "hash"])


class KnowledgeBaseInfo:
    """
    Thin layer to manage the list of files that the LLM takes into account
    for the chat.

    It features the convenience methods to add files, check if a file is already
    a part of the knowledge base, and retrieve the list of files.
    """

    def __init__(self) -> None:
        self._kb_info_by_hash: Dict[str, PdfFileInfo] = {}

    def add(self, pdf_file_info: PdfFileInfo) -> None:
        """
        Adds the knowledge base info to the class attribute.

        Args:
            pdf_file_info (PdfFileInfo): The PDF file info to add.
        """
        self._kb_info_by_hash[pdf_file_info.hash] = pdf_file_info

    def contains(self, hash: str) -> bool:
        """
        Checks if the given hash is present in the knowledge base.

        Args:
            hash (str): The hash to check.

        Returns:
            bool: True if the hash is present in the knowledge base, False
                otherwise.
        """
        return hash in self._kb_info_by_hash

    def get_all(self) -> list[PdfFileInfo]:
        """
        Retrieves all the knowledge base info.

        Returns:
            list[PdfFileInfo]: The list of PDF file info.
        """
        return list(self._kb_info_by_hash.values())

    def size(self) -> int:
        """
        Returns the number of documents in the knowledge base.
        """
        return len(self._kb_info_by_hash)

    def __repr__(self) -> str:
        """
        Returns the developer-friendly string representation of the class
        instance.
        """
        return f"KnowledgeBaseInfo({self._kb_info_by_hash})"
