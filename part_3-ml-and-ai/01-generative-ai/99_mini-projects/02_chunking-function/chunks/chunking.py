"""Chunking functions."""

def chunk_text(text, chunk_size, overlap, split_on_whitespace_only=True):
    """Chunk text into smaller pieces.

    Args:
        text (str): Text to converts into chunks.
        chunk_size (int): Size of each chunk.
        overlap (int): Number of characters to overlap between chunks.
        split_on_whitespace_only (bool): If True, split chunks on whitespace only.

    Returns:
        list: List of text chunks.
    """
    chunks = []
    index = 0

    while index < len(text):
        if split_on_whitespace_only:
            prev_whitespace = 0
            left_index = index - overlap
            while left_index >= 0:
                if text[left_index].isspace():
                    prev_whitespace = left_index
                    break
                left_index -= 1
            next_whitespace = text.find(" ", index + chunk_size)
            if next_whitespace == -1:
                next_whitespace = len(text)
            chunk = text[prev_whitespace:next_whitespace]
            chunks.append(chunk)
            index = next_whitespace + 1
        else:
            start = max(0, index - overlap + 1)
            end = min(index + chunk_size + overlap, len(text))
            chunk = text[start:end].strip()
            chunks.append(chunk)
            index += chunk_size

    return chunks