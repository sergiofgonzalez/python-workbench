"""
Load PDF using pypdf into a list of Document objects

This script requires `pypdf` to be installed.
"""

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

BASE_PATH = Path(__file__).resolve().parents[1]
FILE_PATH = (
    BASE_PATH / "data" / "pdfs" / "cs229_lectures_MachineLearning-Lecture01.pdf"
).resolve()

loader = PyPDFLoader(str(FILE_PATH))
pages = loader.load_and_split()

print(pages[0])
