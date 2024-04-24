"""LLM services for the LLM DocBot app."""

import os

import streamlit as st
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger

from docschat.utils.llm_doctbot_app_helper import ConfigKeys


def load_db(pdf_file_path: str, k: int = 3) -> VectorStoreRetriever:
    """
    Loads the document database with the provided PDF file who should be local
    to the server and returns the Retriever object configured to return k
    documents.

    Args:
        pdf_file_path (str): The path to the PDF file to load.
        k (int): The number of documents to return in the retriever.

    Returns:
        VectorStoreRetriever: The retriever object configured to return k
        documents.
    """
    logger.debug("Loading the document database with '{}'", pdf_file_path)

    # Get the document objects from the PDF file
    loader = PyPDFLoader(pdf_file_path)
    documents = loader.load()
    logger.debug(
        "Loaded {} documents from the {}", len(documents), pdf_file_path
    )

    # Generate the splits from which the embedding vectors will be generated
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150
    )
    splits = text_splitter.split_documents(documents)
    logger.debug(
        "Generated {} splits from the {} documents",
        len(splits),
        len(documents),
    )

    # Create the embeddings function
    embeddings = AzureOpenAIEmbeddings(
        deployment=os.getenv(
            ConfigKeys.AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME.value
        ),
    )
    logger.debug(
        "Embeddings function created successfully: using '{}'",
        os.getenv(ConfigKeys.AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME.value),
    )

    # Configure a DocArray in-memory db for the embeddings
    db = DocArrayInMemorySearch.from_documents(splits, embeddings)

    # Return the associated retriever object
    logger.debug(
        "Returning DocArrayInMemorySearch Vector Store retriever with k={}", k
    )
    return db.as_retriever(k=k)


def get_chat_llm():
    """
    Returns the LLM chat object for the LLM DocBot app. Because we want answers
    from a PDF, the temperature is set to 0.

    Returns:
        AzureChatOpenAI: The Azure OpenAI chat object.
    """
    logger.debug(
        "Creating the LLM chat using '{}'; model='{}'",
        os.getenv(ConfigKeys.AZURE_OPEN_AI_CHAT_DEPLOYMENT_NAME.value),
        os.getenv(ConfigKeys.AZURE_OPEN_AI_CHAT_MODEL_NAME.value),
    )

    return AzureChatOpenAI(
        deployment_name=os.getenv(
            ConfigKeys.AZURE_OPEN_AI_CHAT_DEPLOYMENT_NAME.value
        ),
        model_name=os.getenv(ConfigKeys.AZURE_OPEN_AI_CHAT_MODEL_NAME.value),
        temperature=0,
    )


@st.cache_resource
def get_question_answer_chain(pdf_file_path):
    """Returns the question-answer chain for the LLM DocBot app."""
    retriever = load_db(pdf_file_path)
    llm = get_chat_llm()
    qa = RetrievalQA.from_llm(
        llm=llm, retriever=retriever, return_source_documents=True
    )
    logger.debug(
        "Question-Answer chain created successfully for {}", pdf_file_path
    )

    return qa
