"""
Load audio from YouTube into a list of Document objects

This script requires the following packages:
NOTE: these packages are huge, so you might want to skip them.
+ `transformers`
+ `torch`
+ `yt_dlp`
+ `pydub`
+ `librosa`
+ `openai`
+ `python-dotenv`

Note also that:
+ OpenAIWhisperParser does not support Azure OpenAI.
+ OpenAIWhisperParserLocal fails after some time.
"""

import os
from pathlib import Path

import openai
from dotenv import load_dotenv
from langchain_community.document_loaders.blob_loaders.youtube_audio import (
    YoutubeAudioLoader,
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.audio import (
    OpenAIWhisperParser,
    OpenAIWhisperParserLocal,
)

load_dotenv()

urls = ["https://youtu.be/kCc8FmEb1nY", "https://youtu.be/VMj-3S1tku0"]

BASE_PATH = Path(__file__).resolve().parents[1]
FILE_PATH = (BASE_PATH / "data" / "youtube").resolve()

local = False
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_key = os.getenv("OPENAI_API_KEY")

if local:
    loader = GenericLoader(
        YoutubeAudioLoader(urls, save_dir=str(FILE_PATH)),
        OpenAIWhisperParserLocal(),
    )
else:
    loader = GenericLoader(
        YoutubeAudioLoader(urls, save_dir=str(FILE_PATH)), OpenAIWhisperParser()
    )

docs = loader.load()
