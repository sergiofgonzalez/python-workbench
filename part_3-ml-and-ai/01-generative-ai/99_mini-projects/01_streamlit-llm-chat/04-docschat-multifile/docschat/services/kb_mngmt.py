"""
Knowledge Base Management Service
"""

import hashlib
import tempfile

from loguru import logger

from docschat.models.kb_info import KnowledgeBaseInfo, PdfFileInfo
from docschat.utils.llm_doctbot_app_helper import (
    SessionKeys,
    read_app_state,
    update_app_state,
)


def handle_selected_pdf(pdf_file) -> bool:
    """
    Manages all of the non-UI related activities when a PDF file is selected.

    Args:
        pdf_file (str): The file the user has selected

    Returns:
        True if the file is added to the knowledge base, False otherwise

    """
    kb_info: KnowledgeBaseInfo = read_app_state(SessionKeys.KB_INFO)
    logger.debug("PDF file selected: '{}'", pdf_file.name)
    pdf_bytes = pdf_file.read()
    hash = hashlib.md5(pdf_bytes).hexdigest()
    if kb_info and kb_info.contains(hash):
        logger.debug(
            "PDF file '{}' is already present in the knowledge base: skipping",
            pdf_file.name,
        )
        return False
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(pdf_bytes)

        uploaded_pdf_info = PdfFileInfo(
            friendly_name=pdf_file.name, temp_path=f.name, hash=hash
        )
        kb_info.add(uploaded_pdf_info)
        logger.debug(
            "PDF file info processed and added to the knowledge base: {}",
            uploaded_pdf_info,
        )

    update_app_state(SessionKeys.KB_INFO, kb_info)
    return True
