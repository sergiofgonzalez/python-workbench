"""Illustrates how to use images and audio with LangChain agents."""

import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

load_dotenv()

llm = ChatOpenAI(
    model="bedrock-claude-sonnet-4-5",
    api_key=SecretStr(os.environ["LITELLM_API_KEY"]),
    base_url=os.getenv("LITELLM_BASE_URL"),
)


def agent_image_describer() -> None:
    """Create an agent that can describe images."""
    agent = create_agent(llm)

    img_path = Path("__file__").parent / "pics" / "z1t1KKcZRyS6HUF6yTQW8A.jpg"

    with img_path.open("rb") as f:
        img_bytes = f.read()

    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    multimodal_question = HumanMessage(
        [
            {"type": "text", "text": "Describe the image."},
            {"type": "image", "base64": img_b64, "mime_type": "image/jpeg"},
        ],
    )

    response = agent.invoke(
        {"messages": [multimodal_question]},
    )

    print(response["messages"][-1].content)
    print("-" * 80)


def agent_audio_enabled() -> None:
    """Create an agent that can process audio input."""
    agent = create_agent(llm)

    audio_path = Path("__file__").parent / "audio" / "add_chili_peppers.mp3"

    with audio_path.open("rb") as f:
        audio_bytes = f.read()

    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    multimodal_question = HumanMessage(
        [
            {"type": "text", "text": "Describe the audio."},
            {"type": "audio", "base64": audio_b64, "mime_type": "audio/mp3"},
        ],
    )

    response = agent.invoke(
        {"messages": [multimodal_question]},
    )

    print(response["messages"][-1].content)
    print("-" * 80)


def main() -> None:
    """Application entry point."""
    print("=== Agent that describes images ===")
    agent_image_describer()
    print("=" * 80)

    print("=== Audio conversation with an agent ===")
    agent_audio_enabled()
    print("=" * 80)


if __name__ == "__main__":
    main()
