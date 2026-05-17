"""Illustrates how to get started with Cognee."""

import asyncio
import os
from pathlib import Path

import cognee
from cognee.modules.engine.models.node_set import NodeSet
from dotenv import load_dotenv

load_dotenv()

# create artifacts dir for storing visualization outputs
artifacts_path = ".artifacts"

developer_intro = (
    "Hi, I'm an AI/Backend engineer. "
    "I build FastAPI services with Pydantic, heavy asyncio/aiohttp pipelines, "
    "and production testing via pytest-asyncio. "
    "I've shipped low-latency APIs on AWS, Azure, and GCP."
)

data_dir = Path(__file__).parent / "data"

asset_paths = {
    "human_agent_conversations": str(data_dir / "copilot_conversations.json"),
    "python_zen_principles": str(data_dir / "zen_principles.md"),
    "ontology": str(data_dir / "basic_ontology.owl"),
}

human_agent_conversations = asset_paths["human_agent_conversations"]
python_zen_principles = asset_paths["python_zen_principles"]
ontology_path = asset_paths["ontology"]


async def main() -> None:
    """Async application entry point."""
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    await cognee.add(developer_intro, node_set=["developer_data"])
    await cognee.add(human_agent_conversations, node_set=["developer_data"])
    await cognee.add(python_zen_principles, node_set=["principles_data"])

    # configure ontology file path for structured data processing
    os.environ["ONTOLOGY_FILE_PATH"] = ontology_path

    # transform all the data in the cognee store into a KG backed by embeddings
    await cognee.cognify()

    artifacts_dir = Path(__file__).parent / artifacts_path
    artifacts_dir.mkdir(exist_ok=True)

    # generate the inital graph visualization showing nodesets and ontology structure
    # workaround: cognee.visualize_graph returns the HTML but its internal file write
    # is a missing `await` (bug in cognee), so we write the file ourselves
    initial_graph_html = await cognee.visualize_graph()
    (artifacts_dir / "graph_visualization_nodesets_and_ontology.html").write_text(
        initial_graph_html,
        encoding="utf-8",
    )

    # enhance the knowledge graph with memory consolidation for improved connections
    await cognee.memify()

    # generate the second graph visualization after memory enhancement
    enhanced_graph_html = await cognee.visualize_graph()
    (artifacts_dir / "graph_visualization_after_memify.html").write_text(
        enhanced_graph_html,
        encoding="utf-8",
    )

    # demonstrate cross-document knowledge retrieval from multiple data sources
    results = await cognee.search(
        query_text="How my AsyncWebScraper implementation align with Python's design principles?",  # noqa: E501
        query_type=cognee.SearchType.GRAPH_COMPLETION,
    )
    print("Python Pattern Analysis:", results)

    # demonstrate filtered search using NodeSet to query only specific subsets of memory
    results = await cognee.search(
        query_text="How should variables be named?",
        query_type=cognee.SearchType.GRAPH_COMPLETION,
        node_type=NodeSet,
        node_name=["principles_data"],
    )
    print("Filtered search result:", results)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run
    asyncio.run(main())
