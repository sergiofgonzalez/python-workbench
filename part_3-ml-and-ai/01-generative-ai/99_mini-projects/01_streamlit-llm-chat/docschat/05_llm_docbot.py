"""Streamlit application of bot that interacts with an LLM"""

import os
import tempfile
import time

import streamlit as st
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

if "config_loaded" not in st.session_state:
    load_dotenv()
    st.session_state.config_loaded = True


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




def response_generator(message, qa):
    """
    Returns a generator function with the response from the LLM
    """
    llm_response = qa({"query": message})
    for word in llm_response["result"].split():
        yield word + " "
        time.sleep(0.02)


def load_db(file_path, k=3):
    # Load documents from file
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # Generate splits
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    splits = text_splitter.split_documents(documents)

    # Create the embeddings function
    embeddings = AzureOpenAIEmbeddings(
        deployment=os.getenv("AZURE_OPENAI_TEXT_EMBEDDING_DEPLOYMENT_NAME")
    )

    # Get an in-memory vector db with the existing splits and embedding function
    db = DocArrayInMemorySearch.from_documents(splits, embeddings)

    # Instantiate the retriever
    retriever = db.as_retriever(k=k)


    # Instantiate the LLM
    llm = AzureChatOpenAI(
        deployment_name=os.getenv("AZURE_OPEN_AI_CHAT_DEPLOYMENT_NAME"),
        model_name=os.getenv("AZURE_OPEN_AI_CHAT_MODEL_NAME"),
        temperature=0,
    )

    # Return a chatbot chain, with memory managed externally
    qa = RetrievalQA.from_llm(
        llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa

st.title("LLM PDF Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Check if file has already been selected
# if "file_selected" not in st.session_state:
#     uploaded_pdf = st.file_uploader("Upload a PDF...", type=["pdf"])
#     if uploaded_pdf is not None:
#         st.session_state.file_selected = True
#         st.session_state.pdf_filename = uploaded_pdf.name
#         pdf_bytes = uploaded_pdf.read()
#         with tempfile.NamedTemporaryFile(delete=False) as f:
#             f.write(pdf_bytes)
#             st.session_state.file_path = f.name

uploaded_pdf = st.file_uploader("Upload a PDF...", type=["pdf"])
if uploaded_pdf is not None:
    st.session_state.file_selected = True
    st.session_state.pdf_filename = uploaded_pdf.name
    pdf_bytes = uploaded_pdf.read()
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(pdf_bytes)
        st.session_state.file_path = f.name
else:
    # Clean session state as file has either not been selected or has been removed
    st.session_state.pop("file_selected", None)
    st.session_state.pop("pdf_filename", None)
    st.session_state.pop("file_path", None)
    if "messages" in st.session_state:
        st.session_state.messages = []

if "file_path" in st.session_state:
    qa = load_db(st.session_state.file_path)

# Display chat history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if "file_path" not in st.session_state:
    st.stop()

if prompt := st.chat_input(f"Type something here to talk to {st.session_state.pdf_filename}..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display bot response
    with st.chat_message("assistant"):
        st.write("Thinking...")

        response = st.write_stream(response_generator(prompt, qa))

    st.session_state.messages.append({"role": "assistant", "content": response})
