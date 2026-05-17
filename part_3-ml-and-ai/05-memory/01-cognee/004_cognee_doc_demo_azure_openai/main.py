"""Illustrates how to get started with Cognee."""

import asyncio
from pathlib import Path

import cognee
from dotenv import load_dotenv

load_dotenv()

data_dir = Path(__file__).parent / "data"
file_path = data_dir / "alice_in_wonderland.txt"


async def main() -> None:
    """Async application entry point."""
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    # tell cognee to process document
    await cognee.add(file_path)

    # transform all the data in the cognee store into a KG backed by embeddings
    await cognee.cognify()

    # query cognee for information from provided document
    answer = await cognee.search(
        "List me all the important characters in Alice in Wonderland.",
    )
    print("Answer to query:", answer)

    answer = await cognee.search(
        "How did Alice end up in Wonderland?",
    )
    print("Answer to query:", answer)

    answer = await cognee.search(
        "Tell me about Alice's personality.",
    )
    print("Answer to query:", answer)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run
    asyncio.run(main())
