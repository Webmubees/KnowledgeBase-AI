from pathlib import Path

from chunking import chunk_text
from loaders.router import load_file


DOCUMENTS_DIR = Path(
    "data/documents"
)


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx"
}


def load_documents():

    documents = []

    for file_path in DOCUMENTS_DIR.iterdir():

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        print(
            f"Loading: {file_path.name}"
        )

        text = load_file(
            file_path
        )

        chunks = chunk_text(
            text
        )

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
                        )
                }
            )

    return documents