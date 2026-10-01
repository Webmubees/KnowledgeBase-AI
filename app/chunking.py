def chunk_text(
    text,
    chunk_size=500,
    overlap=50
):
    """
    Split text into chunks while trying
    to preserve paragraph boundaries.
    """

    text = text.strip()

    if not text:
        return []

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        # If adding this paragraph keeps us
        # within the chunk size, add it.
        if len(current_chunk) + len(paragraph) + 1 <= chunk_size:

            if current_chunk:
                current_chunk += "\n"

            current_chunk += paragraph

        else:

            if current_chunk:
                chunks.append(
                    current_chunk.strip()
                )

            # Handle paragraphs that are themselves
            # larger than the chunk size.
            if len(paragraph) > chunk_size:

                start = 0

                while start < len(paragraph):

                    end = start + chunk_size

                    chunks.append(
                        paragraph[start:end].strip()
                    )

                    start = end - overlap

                current_chunk = ""

            else:
                current_chunk = paragraph

    # Add final chunk
    if current_chunk:
        chunks.append(
            current_chunk.strip()
        )

    return chunks