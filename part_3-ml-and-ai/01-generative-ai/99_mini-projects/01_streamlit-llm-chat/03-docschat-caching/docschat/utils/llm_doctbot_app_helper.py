"""
Helper elements for the LLM DoctBot app
"""

from enum import Enum

import streamlit as st
from loguru import logger


class SessionKeys(Enum):
    IS_CONFIG_LOADED = "flag_config_loaded"
    IS_CHAT_READY = "flag_chat_ready"
    PDF_FILE_INFO = "pdf_file_info"
    MESSAGE_HISTORY = "message_history"


class ConfigKeys(Enum):
    LOG_LEVEL = "DOCSCHAT_LOG_LEVEL"
    AZURE_OPENAI_API_KEY = "AZURE_OPENAI_API_KEY"
    AZURE_OPEN_AI_CHAT_DEPLOYMENT_NAME = "AZURE_OPEN_AI_CHAT_DEPLOYMENT_NAME"
    AZURE_OPEN_AI_CHAT_MODEL_NAME = "AZURE_OPEN_AI_CHAT_MODEL_NAME"
    AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME = (
        "AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME"
    )


def update_app_state(session_key: SessionKeys, session_value: any) -> None:
    """
    Updates the session state with the provided key and value.

    Args:
        session_key (SessionKeys): The key to update in the session state.
        session_value (any): The value to update in the session state.
    """
    logger.debug(
        "Updating session state: {}={}", session_key.value, session_value
    )
    st.session_state[session_key.value] = session_value


def read_app_state(session_key: SessionKeys) -> any:
    """
    Reads the session state with the provided key.

    Args:
        session_key (SessionKeys): The key to read from the session state.

    Returns:
        any: The value of the key in the session state, or None if the key is not
        present in the session state.
    """
    if session_key.value not in st.session_state:
        logger.debug("Session state: key {} not found", session_key.value)
        return None
    logger.debug(
        "Reading session state: {}: {}",
        session_key.value,
        st.session_state[session_key.value],
    )
    return st.session_state[session_key.value]
