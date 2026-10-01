from pathlib import Path

from chunking import chunk_text


DOCUMENTS_DIR = Path("data/documents")


def load_documents():

    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):

        text = file_path.read_text(
            encoding="utf-8"
        )

        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):

            documents.append(
                {
                    "source": file_path.name,
                    "chunk": index,
                    "text": chunk
                }
            )

    return documents