"""Illustrates how to get started with Cognee."""

import asyncio
from pathlib import Path

import cognee
from cognee.api.v1.visualize.visualize import visualize_graph
from cognee.modules.recall.types.RecallResponse import ResponseQAEntry
from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    """Async application entry point."""
    # store permanently in the KG
    # (behind the scenes, Cognee will run add + cognify + improve)
    await cognee.remember("Cognee turns documents into AI memory.")

    # store in session memory only
    # (fast cache, syncs to KG in the background)
    await cognee.remember("User prefer detailed explanations.", session_id="chat_1")

    graph_path = Path(__file__).parent / "graph.html"
    initial_graph_html = await visualize_graph()
    graph_path.write_text(
        initial_graph_html,
        encoding="utf-8",
    )

    # Query Cognee, letting it decide the best search strategy
    results = await cognee.recall("What does the user prefer?", session_id="chat_1")
    for result in results:
        if isinstance(result, ResponseQAEntry):
            print(result.answer)

    # Delete once done
    await cognee.forget(dataset="main_dataset")


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run
    asyncio.run(main())
