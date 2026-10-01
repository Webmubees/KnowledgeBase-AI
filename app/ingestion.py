from pathlib import Path

from chunking import chunk_text
from loaders.router import load_file


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx"
}


def load_document(
    file_path: Path
):

    if (
        file_path.suffix.lower()
        not in SUPPORTED_EXTENSIONS
    ):
        return []

    print(
        f"Loading: {file_path.name}"
    )

    text = load_file(
        file_path
    )

    chunks = chunk_text(
        text
    )

    documents = []

    for index, chunk in enumerate(
        chunks
    ):

        documents.append(
            {
                "source": file_path.name,

                "chunk": index,

                "text": chunk,

                "document_type":
                    file_path.suffix.lower().replace(
                        ".",
                        ""
                    ),

                "page": None
            }
        )

    return documents