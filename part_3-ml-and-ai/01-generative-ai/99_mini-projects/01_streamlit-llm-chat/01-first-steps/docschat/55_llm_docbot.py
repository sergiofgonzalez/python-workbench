"""Streamlit application of bot that lets you chat with a document via an LLM"""

import os
import time

import streamlit as st
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

if "config_loaded" not in st.session_state:
    load_dotenv()
    st.session_state.config_loaded = True

if "AZURE_OPENAI_ENDPOINT" not in st.config:
    st.error(
        "Please add your Azure OpenAI endpoint to your configuration as "
        "`AZURE_OPENAI_ENDPOINT`."
    )
    st.stop()


if "AZURE_OPENAI_API_KEY" not in st.secrets:
    st.error(
        "Please add your Azure OpenAI API key to secrets as "
        "`AZURE_OPEN_API_KEY`."
    )
    st.stop()

if not os.getenv("AZURE_OPEN_AI_CHAT_DEPLOYMENT_NAME"):
    st.error(
        "Please add your Azure OpenAI Chat deployment name to your "
        "configuration as `AZURE_OPEN_AI_CHAT_DEPLOYMENT_NAME`."
    )
    st.stop()

if not os.getenv("AZURE_OPEN_AI_CHAT_MODEL_NAME"):
    st.error(
        "Please add your Azure OpenAI Chat model name to your "
        "configuration as `AZURE_OPEN_AI_CHAT_MODEL_NAME`."
    )
    st.stop()

llm = AzureChatOpenAI(
    deployment_name=os.getenv("AZURE_OPEN_AI_CHAT_DEPLOYMENT_NAME"),
    model_name=os.getenv("AZURE_OPEN_AI_CHAT_MODEL_NAME"),
    temperature=0
)

def response_generator(message):
    """
    Returns a generator function with the response from the LLM
    """
    human_message = HumanMessage(message)
    llm_response = llm.invoke([message])
    for word in llm_response.content.split():
        yield word + " "
        time.sleep(0.02)


st.title("LLM Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Let the user select a file to talk to
uploaded_pdf = st.file_uploader("Select a PDF file", type="pdf")
if uploaded_pdf is not None:
    st.write("You selected the following PDF file:")
    st.write(uploaded_pdf)

    # # Extract text from PDF
    # text = ""
    # with st.spinner("Extracting text from PDF..."):
    #     text = st.pdf_reader(uploaded_pdf)

    # # Display extracted text
    # st.write(text)

    # Initialize LLM with extracted text
    llm = AzureChatOpenAI(
        deployment_name=os.getenv("AZURE_OPEN_AI_CHAT_DEPLOYMENT_NAME"),
        model_name=os.getenv("AZURE_OPEN_AI_CHAT_MODEL_NAME"),
        temperature=0,
        text=text
    )

    # Reset chat history
    st.session_state.messages = []

# Display chat history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Type something here..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display bot response
    with st.chat_message("assistant"):
        st.write("Thinking...")

        response = st.write_stream(response_generator(prompt))

    st.session_state.messages.append({"role": "assistant", "content": response})
