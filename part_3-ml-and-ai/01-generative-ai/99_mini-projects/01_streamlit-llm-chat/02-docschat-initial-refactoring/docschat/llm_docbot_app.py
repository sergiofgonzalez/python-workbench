"""
Entry point for Streamlit LLM DocBot application that lets you chat with a PDF
via an LLM.
"""

import os
import sys
import tempfile
import time

import streamlit as st
from dotenv import load_dotenv
from loguru import logger

from docschat.models.pdf_file_info import PdfFileInfo
from docschat.services.llm import get_question_answer_chain
from docschat.utils.llm_doctbot_app_helper import (
    ConfigKeys,
    SessionKeys,
    read_app_state,
    update_app_state,
)

# Load the environment variables
load_dotenv()

# Set the logger level
logger.remove()
logger.add(sys.stderr, level=os.getenv(ConfigKeys.LOG_LEVEL.value, "DEBUG"))


def validate_config():
    """
    Validates the configuration settings for the application.

    If any error is found, it will be displayed and the application will stop.
    """
    logger.debug("Validating configuration settings...")

    init_errors = False
    if ConfigKeys.AZURE_OPENAI_API_KEY.value not in st.secrets:
        st.error(
            "Please add your Azure OpenAI API key to secrets as "
            "`AZURE_OPENAI_API_KEY`."
        )
        init_errors = True
        logger.error(
            "{} not found in secrets", ConfigKeys.AZURE_OPENAI_API_KEY.value
        )

    if not os.getenv(ConfigKeys.AZURE_OPEN_AI_CHAT_DEPLOYMENT_NAME.value):
        st.error(
            "Please add your Azure OpenAI Chat deployment name to your "
            "configuration as `AZURE_OPEN_AI_CHAT_DEPLOYMENT_NAME`."
        )
        init_errors = True
        logger.error(
            "{} not found in the environment",
            ConfigKeys.AZURE_OPEN_AI_CHAT_DEPLOYMENT_NAME.value,
        )

    if not os.getenv(ConfigKeys.AZURE_OPEN_AI_CHAT_MODEL_NAME.value):
        st.error(
            "Please add your Azure OpenAI Chat model name to your "
            "configuration as `AZURE_OPEN_AI_CHAT_MODEL_NAME`."
        )
        init_errors = True
        logger.error(
            "{} not found in the environment",
            ConfigKeys.AZURE_OPEN_AI_CHAT_MODEL_NAME.value,
        )

    if not os.getenv(ConfigKeys.AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME.value):
        st.error(
            "Please add your Azure OpenAI Chat model name to your "
            "configuration as `AZURE_OPEN_AI_CHAT_MODEL_NAME`."
        )
        init_errors = True
        logger.error(
            "{} not found in the environment",
            ConfigKeys.AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME.value,
        )

    if init_errors:
        st.stop()
    logger.debug("Configuration settings validated.")


def init_session():
    """Initializes the session state if not already initialized"""
    logger.debug("Reading configuration values from .env")
    load_dotenv()
    validate_config()
    update_app_state(SessionKeys.IS_CONFIG_LOADED, True)
    update_app_state(SessionKeys.MESSAGE_HISTORY, [])


def show_file_selector():
    """Displays a file selector for the user to upload a PDF"""
    logger.debug("Displaying the file selector...")
    uploaded_pdf = st.file_uploader("Upload a PDF...", type=["pdf"])
    if uploaded_pdf is not None:
        logger.debug("The PDF file {} is currently selected", uploaded_pdf.name)
        pdf_bytes = uploaded_pdf.read()
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(pdf_bytes)
            uploaded_pdf_info = PdfFileInfo(
                friendly_name=uploaded_pdf.name, temp_path=f.name
            )
            logger.debug("PDF file info: {}", uploaded_pdf_info)
        update_app_state(SessionKeys.PDF_FILE_INFO, uploaded_pdf_info)
        update_app_state(SessionKeys.IS_CHAT_READY, True)
    else:
        # Clean uploaded PDF file info as file has either not been selected yet
        # or has been removed after selection.
        logger.debug("PDF file not selected or cleared: cleaning app state...")
        update_app_state(SessionKeys.PDF_FILE_INFO, None)
        update_app_state(SessionKeys.MESSAGE_HISTORY, [])
        update_app_state(SessionKeys.IS_CHAT_READY, False)


def show_chat_messages():
    """Displays the message history in the chat_message element"""
    logger.debug("Retrieving and displaying chat messages from history...")
    for message in read_app_state(SessionKeys.MESSAGE_HISTORY):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    logger.debug("Chat messages displayed.")


def response_generator(message):
    """
    Returns a generator function with the response from the LLM, yielding word
    by word with a certain delay to emulate typing.
    """
    logger.debug("Yielding response word by word from message: {}", message)
    for word in message.split():
        yield word + " "
        time.sleep(0.02)


def handle_llm_chat():
    """Manages the chat interaction with the LLM"""
    # Display the chat messages
    logger.debug("Handling the LLM chat interactions...")
    show_chat_messages()
    qa = get_question_answer_chain(
        read_app_state(SessionKeys.PDF_FILE_INFO).temp_path
    )
    logger.debug(
        "QA chain created with {}",
        read_app_state(SessionKeys.PDF_FILE_INFO).temp_path,
    )

    logger.debug("Displaying the chat prompt...")
    if prompt := st.chat_input(
        "Type something here to talk to "
        f"{read_app_state(SessionKeys.PDF_FILE_INFO).friendly_name}..."
    ):
        logger.debug("About to process user input: {}", prompt)

        with st.chat_message("user"):
            st.markdown(prompt)

        # Get the response from the LLM
        llm_response = qa({"query": prompt})
        logger.debug(
            "LLM response: {}: {}",
            llm_response["query"],
            llm_response["result"],
        )

        # Display bot response
        with st.chat_message("assistant"):
            response = st.write_stream(
                response_generator(llm_response["result"])
            )

        # Update the message history in the app state
        message_history = read_app_state(SessionKeys.MESSAGE_HISTORY)
        message_history.append({"role": "user", "content": prompt})
        message_history.append({"role": "assistant", "content": response})
        update_app_state(SessionKeys.MESSAGE_HISTORY, message_history)


if __name__ == "__main__":
    logger.debug("Refreshing the app...")
    st.title("LLM PDF Bot")
    if not read_app_state(SessionKeys.IS_CONFIG_LOADED):
        init_session()
    show_file_selector()
    if read_app_state(SessionKeys.IS_CHAT_READY):
        handle_llm_chat()
    logger.debug("App refreshed.")
