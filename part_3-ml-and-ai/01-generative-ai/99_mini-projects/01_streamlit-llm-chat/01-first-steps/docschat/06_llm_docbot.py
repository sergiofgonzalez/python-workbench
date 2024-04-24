"""
Entry point for Streamlit LLM DocBot application that lets you chat with a PDF
via an LLM.
"""

import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Globals
IS_CONFIG_LOADED_KEY = "flag_config_loaded"
AZURE_OPENAI_API_KEY_ENVVAR = "AZURE_OPENAI_API_KEY"
AZURE_OPEN_AI_CHAT_DEPLOYMENT_NAME_ENVVAR = "AZURE_OPEN_AI_CHAT_DEPLOYMENT_NAME"
AZURE_OPEN_AI_CHAT_MODEL_NAME_ENVVAR = "AZURE_OPEN_AI_CHAT_MODEL_NAME"


def validate_config():
    """
    Validates the configuration settings for the application.

    If any error is found, it will be displayed and the application will stop.
    """
    init_errors = False
    if AZURE_OPENAI_API_KEY_ENVVAR not in st.secrets:
        st.error(
            "Please add your Azure OpenAI API key to secrets as "
            "`AZURE_OPEN_API_KEY`."
        )
        init_errors = True

    if not os.getenv(AZURE_OPEN_AI_CHAT_DEPLOYMENT_NAME_ENVVAR):
        st.error(
            "Please add your Azure OpenAI Chat deployment name to your "
            "configuration as `AZURE_OPEN_AI_CHAT_DEPLOYMENT_NAME`."
        )
        init_errors = True

    if not os.getenv(AZURE_OPEN_AI_CHAT_MODEL_NAME_ENVVAR):
        st.error(
            "Please add your Azure OpenAI Chat model name to your "
            "configuration as `AZURE_OPEN_AI_CHAT_MODEL_NAME`."
        )
        init_errors = True

    if init_errors:
        st.stop()


def init_session():
    """Initializes the session state if not already initialized"""
    if IS_CONFIG_LOADED_KEY not in st.session_state:
        load_dotenv()
        validate_config()
        st.session_state.messages = []
        st.session_state[IS_CONFIG_LOADED_KEY] = True


def show_file_selector():
    """Displays a file selector for the user to upload a PDF"""
    uploaded_pdf = st.file_uploader("Upload a PDF...", type=["pdf"])
    # if uploaded_pdf is not None:
    #     st.session_state.file_selected = True
    #     st.session_state.pdf_filename = uploaded_pdf.name
    #     pdf_bytes = uploaded_pdf.read()
    #     with tempfile.NamedTemporaryFile(delete=False) as f:
    #         f.write(pdf_bytes)
    #         st.session_state.file_path = f.name
    # else:
    #     # Clean session state as file has either not been selected or has been removed
    #     st.session_state.pop("file_selected", None)
    #     st.session_state.pop("pdf_filename", None)
    #     st.session_state.pop("file_path", None)
    #     if "messages" in st.session_state:
    #         st.session_state.messages = []


if __name__ == "__main__":
    init_session()
    st.title("LLM PDF Bot")
    show_file_selector()
