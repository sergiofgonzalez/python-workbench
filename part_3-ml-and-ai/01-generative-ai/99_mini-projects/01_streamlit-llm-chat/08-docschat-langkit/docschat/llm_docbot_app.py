"""
Entry point for Streamlit LLM DocBot application that lets you chat with a PDF
via an LLM.
"""

import os
import sys
import time

import streamlit as st
from dotenv import load_dotenv
from loguru import logger

from docschat.models.kb_info import KnowledgeBaseInfo
from docschat.services.errors import (
    PromptSecurityRiskError,
    ResponseRelevanceError,
    ResponseSecurityRiskError,
)
from docschat.services.kb_mngmt import handle_selected_pdf
from docschat.services.llm import get_question_answer_chain
from docschat.services.responsible_ai import (
    RAI,
    evaluate_prompt,
    evaluate_response,
)
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


def update_session_after_kb_update(new_kb_info, chat_ready):
    logger.debug("KB updated: cleaning app state...")
    update_app_state(SessionKeys.KB_INFO, new_kb_info)
    update_app_state(SessionKeys.MESSAGE_HISTORY, [])
    update_app_state(SessionKeys.IS_CHAT_READY, chat_ready)


def show_file_selector():
    """Displays a file selector for the user to upload one or more PDFs"""
    logger.debug("Displaying the file selector...")
    selected_pdfs = st.file_uploader(
        "Upload PDF files...", type=["pdf"], accept_multiple_files=True
    )
    if selected_pdfs and len(selected_pdfs) != 0:
        handled = [
            handle_selected_pdf(selected_pdf) for selected_pdf in selected_pdfs
        ]
        kb_info = read_app_state(SessionKeys.KB_INFO)
        diff_size = len(selected_pdfs) != kb_info.size()

        if any(handled) or diff_size:
            update_app_state(SessionKeys.KB_UPDATED, True)
            update_session_after_kb_update(kb_info, chat_ready=True)
        else:
            update_app_state(SessionKeys.IS_CHAT_READY, True)
            update_app_state(SessionKeys.KB_UPDATED, False)
    else:
        logger.debug("PDF files not selected: cleaning app state...")
        update_session_after_kb_update(KnowledgeBaseInfo(), chat_ready=False)


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


def is_prompt_ok(rai_enhanced_prompt):
    """Simple way of checking if the prompt is ok to be sent to the LLM."""
    return rai_enhanced_prompt[RAI.PROMPT_SECURITY_RISK.value] == 0


def is_response_ok(rai_enhanced_response):
    """
    Simple way of checking if the response is ok to be displayed to the user.
    """
    return rai_enhanced_response[RAI.RESPONSE_SECURITY_RISK.value] == 0


def handle_llm_chat():
    """Manages the chat interaction with the LLM"""
    # Display the chat messages
    logger.debug("Handling the LLM chat interactions...")
    show_chat_messages()

    # poor man's caching due to temporary file names
    if read_app_state(SessionKeys.KB_UPDATED):
        logger.debug("Rebuilding QA chain as KB has changed since last time")
        with st.spinner("Please wait while building the knowledge base..."):
            pdf_file_paths = [
                pdf.temp_path
                for pdf in read_app_state(SessionKeys.KB_INFO).get_all()
            ]
            qa = get_question_answer_chain(pdf_file_paths)
            update_app_state(SessionKeys.QA_LLM, qa)
            logger.debug(
                "QA chain created with {} and added to the session",
                read_app_state(SessionKeys.KB_INFO),
            )

    qa = read_app_state(SessionKeys.QA_LLM)
    logger.debug("Displaying the chat prompt...")
    if prompt := st.chat_input(
        "Type something here to talk to the knowledge base"
    ):
        logger.debug("About to process user input: {}", prompt)

        with st.chat_message("user"):
            st.markdown(prompt)

        # Get the response from the LLM
        try:
            if os.getenv(ConfigKeys.RESPONSIBLE_AI_SWITCH.value):
                rai_enhanced_prompt = evaluate_prompt(prompt)
                if not is_prompt_ok(rai_enhanced_prompt):
                    raise PromptSecurityRiskError(
                        f"The prompt '{rai_enhanced_prompt['prompt']}' was "
                        "considered a security risk: "
                        f"risk={rai_enhanced_prompt[RAI.PROMPT_SECURITY_RISK.value]}"  # pylint: disable=C0301:line-too-long
                    )

            llm_response = qa({"question": prompt})
            logger.debug(
                "LLM response: {}: {}",
                llm_response["question"],
                llm_response["answer"],
            )

            if os.getenv(ConfigKeys.RESPONSIBLE_AI_SWITCH.value):
                rai_enhanced_response = evaluate_response(
                    llm_response["answer"], llm_response["question"]
                )
                if not is_response_ok(rai_enhanced_response):
                    raise ResponseSecurityRiskError(
                        f"The response {rai_enhanced_response['response']} was"
                        "considered a security risk:"
                        f"risk={rai_enhanced_response[RAI.RESPONSE_SECURITY_RISK.value]}"  # pylint: disable=C0301:line-too-long
                    )

                if (
                    rai_enhanced_response[
                        RAI.RESPONSE_RELEVANCE_TO_PROMPT_TEXT.value
                    ]
                    == "low"
                ):
                    raise ResponseRelevanceError(
                        f"The response '{rai_enhanced_response['response']} was"
                        "considered not relevant for the question "
                        f"'{rai_enhanced_prompt['prompt']}'."
                    )

        except PromptSecurityRiskError as e:
            logger.error(
                "Security risk identified in the prompt: {}",
                e,
            )
            llm_response = {
                "answer": "Hmm, that prompt didn't conform to our application "
                "Responsible AI policies. Please, try rephrasing."
            }
        except ResponseSecurityRiskError as e:
            logger.error("Security risk identified in the response: {}", e)
            llm_response = {
                "answer": "Unfortunately, the response did not conform to our "
                "application Responsible AI policies. Please, try rephrasing "
                " your question."
            }
        except ResponseRelevanceError as e:
            logger.error("LLM response was considered not relevant: {}", e)
            llm_response = {
                "answer": "I couldn't find a relevant answer to your question. "
                "Can you please try asking your question in a different way?"
            }
        except Exception as e:  # pylint: disable=W0718:broad-exception-caught
            logger.error(
                "An error occurred while processing the LLM request: {}", e
            )
            llm_response = {
                "answer": "Hmm, I didn't quite get an answer to that. "
                "Please, try rephrasing."
            }

        # Display bot response
        with st.chat_message("assistant"):
            response = st.write_stream(
                response_generator(llm_response["answer"])
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
