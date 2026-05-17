"""Illustrates how to get started with Cognee."""

import asyncio

import cognee
import litellm
from cognee.modules.recall.types.RecallResponse import ResponseQAEntry

# Embeddings go LiteLLM-client -> LiteLLM-proxy -> Bedrock (Cohere v3). Two
# defaults from cognee/litellm break that route:
#   - dimensions=N translates to Bedrock's output_dimension, which Cohere v3
#     rejects (fixed 1024-dim output).
#   - encoding_format is sent as a string and translated to embedding_types
#     as a string; Bedrock requires a JSON array.
# Strip both and explicitly send embedding_types=["float"].
_original_aembedding = litellm.aembedding


async def _bedrock_compat_aembedding(*args: object, **kwargs: object) -> object:
    kwargs.pop("dimensions", None)
    kwargs.pop("encoding_format", None)
    kwargs["embedding_types"] = ["float"]
    return await _original_aembedding(*args, **kwargs)


litellm.aembedding = _bedrock_compat_aembedding


async def main() -> None:
    """Async application entry point."""
    # store permanently in the KG
    # (behind the scenes, Cognee will run add + cognify + improve)
    await cognee.remember("Cognee turns documents into AI memory.")

    # store in session memory only
    # (fast cache, syncs to KG in the background)
    await cognee.remember("User prefer detailed explanations.", session_id="chat_1")

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
