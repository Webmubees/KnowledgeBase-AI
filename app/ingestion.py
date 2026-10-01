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

        pages = load_file(
            file_path
        )

        for page_data in pages:

            text = page_data["text"]
            page_number = page_data["page"]

            chunks = chunk_text(
                text
            )

            for chunk_index, chunk in enumerate(
                chunks
            ):

                documents.append(
                    {
                        "source": file_path.name,
                        "chunk": chunk_index,
                        "text": chunk,
                        "page": page_number,
                        "document_type":
                            file_path.suffix.lower().replace(
                                ".",
                                ""
                            )
                    }
                )

    return documents