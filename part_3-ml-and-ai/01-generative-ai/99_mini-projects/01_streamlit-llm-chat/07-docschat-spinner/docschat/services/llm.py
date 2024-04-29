"""LLM services for the LLM DocBot app."""

import os

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader  # type: ignore
# fmt: off
from langchain_community.vectorstores import \
    DocArrayInMemorySearch  # type: ignore
# fmt: on
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger

from docschat.utils.llm_doctbot_app_helper import ConfigKeys

_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

prompt_template = """You are given a document or set of documents in the context. Use the following pieces of context source from a document or documents to answer the question at the end, in its original language. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Helpful Answer:"""


QA_PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)


def load_db(pdf_file_paths: str, k: int = 3) -> VectorStoreRetriever:
    """
    Loads the document database with the provided PDF files who should be local
    to the server and returns the Retriever object configured to return k
    documents.

    Args:
        pdf_file_paths (str): A list with the paths to the PDF files to load.
        k (int): The number of documents to return in the retriever.

    Returns:
        VectorStoreRetriever: The retriever object configured to return k
        documents.
    """
    logger.debug("Loading the document database with '{}'", pdf_file_paths)

    # Get the document objects from the PDF file
    loaders = [PyPDFLoader(pdf_file_path) for pdf_file_path in pdf_file_paths]
    documents = []
    for loader in loaders:
        documents.extend(loader.load())
    logger.debug(
        "Loaded {} documents from {} PDF file(s)",
        len(documents),
        len(pdf_file_paths),
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
        deployment=os.getenv(  # type: ignore
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
        deployment_name=os.getenv(  # type: ignore
            ConfigKeys.AZURE_OPEN_AI_CHAT_DEPLOYMENT_NAME.value
        ),
        model_name=os.getenv(  # type: ignore
            ConfigKeys.AZURE_OPEN_AI_CHAT_MODEL_NAME.value
        ),
        temperature=0,
    )


def get_conversation_memory():
    """
    Returns the conversation memory object for the LLM DocBot app.

    Returns:
        ConversationBufferMemory: The conversation memory object.
    """
    logger.debug("Creating the conversation memory object")
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
    )


def get_question_answer_chain(pdf_file_paths):
    """Returns the question-answer chain for the LLM DocBot app."""
    retriever = load_db(pdf_file_paths)
    llm = get_chat_llm()
    memory = get_conversation_memory()
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT},
        # qa_prompt=QA_PROMPT,
    )
    logger.debug(
        "Conversation Question-Answer chain created successfully for {}",
        pdf_file_paths,
    )

    return qa
