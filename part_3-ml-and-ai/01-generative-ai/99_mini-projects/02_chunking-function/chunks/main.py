"""Testing the chunking with an example"""

from dotenv import load_dotenv

load_dotenv()

from chunks.chunking import chunk_text
from chunks.embedding import embed

if __name__ == "__main__":

    # Simple text with small values for chunk_size and overlap
    text = (
        # "This is a test sentence. It is used for testing the chunking function."
        "AWS Bedrock"
    )
    chunk_size = 10
    overlap = 5
    chunks = chunk_text(text, chunk_size, overlap)
    print(chunks)
    print(f"{len(chunks)!r}")

    # Getting the embeddings for the sample chunks
    embeddings = embed(chunks)
    print(len(embeddings))
    print(len(embeddings[0]))
    print(embeddings[0])
