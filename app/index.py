
from pathlib import Path

from .loaders.router import load_file
from .chunking import chunk_text
from .embeddings import create_embeddings
from .vector_store import add_documents, delete_document
from .document_registry import (
    load_registry,
    save_registry,
    get_file_status,
    update_registry,
    remove_from_registry
)


DOCUMENTS_DIR = Path(
    "data/documents"
)


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx"
}


def main():

    # --------------------------------
    # 1. Load document registry
    # --------------------------------

    registry = load_registry()

    files_to_process = []

    print("Checking documents...\n")


    # --------------------------------
    # 2. Check current documents
    # --------------------------------

    current_files = set()

    for file_path in DOCUMENTS_DIR.iterdir():

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        current_files.add(
            file_path.name
        )

        status = get_file_status(
            file_path,
            registry
        )

        print(
            f"{file_path.name}: {status}"
        )


        # ----------------------------
        # New document
        # ----------------------------

        if status == "new":

            files_to_process.append(
                file_path
            )


        # ----------------------------
        # Modified document
        # ----------------------------

        elif status == "modified":

            print(
                f"Removing old vectors for "
                f"{file_path.name}"
            )

            delete_document(
                file_path.name
            )

            files_to_process.append(
                file_path
            )


    # --------------------------------
    # 3. Detect deleted documents
    # --------------------------------

    registered_files = set(
        registry.keys()
    )

    deleted_files = (
        registered_files - current_files
    )


    for filename in deleted_files:

        print(
            f"{filename}: deleted"
        )

        print(
            f"Removing vectors for "
            f"{filename}"
        )

        delete_document(
            filename
        )

        del registry[filename]


    # --------------------------------
    # 4. No new/modified documents
    # --------------------------------

    if not files_to_process:

        save_registry(
            registry
        )

        if deleted_files:

            print(
                "\nDeleted documents cleaned "
                "from the knowledge base."
            )

        else:

            print(
                "\nNo new or modified documents."
            )

        return


    # --------------------------------
    # 5. Process documents
    # --------------------------------

    print(
        f"\nProcessing "
        f"{len(files_to_process)} document(s)..."
    )

    documents = []


    for file_path in files_to_process:

        print( f"Loading: {file_path.name}")

        # Load document
        loaded_data = load_file(file_path)

        # ==================================
        # PDF
        # ==================================

        if file_path.suffix.lower() == ".pdf":

            for page_data in loaded_data:

                page_number = page_data["page"]

                text = page_data["text"]

                chunks = chunk_text(
                    text
                )

                for index, chunk in enumerate(chunks):

                    documents.append({

                        "source": file_path.name,

                        "chunk": index,

                        "text": chunk,

                        "document_type": "pdf",

                        "page": page_number

                    })

          # ==================================
        # TXT / DOCX
        # ==================================

        else:

            text = loaded_data

            chunks = chunk_text(
                text
            )

            for index, chunk in enumerate(chunks):

                documents.append({

                    "source": file_path.name,

                    "chunk": index,

                    "text": chunk,

                    "document_type":
                        file_path.suffix
                        .lower()
                        .replace(".", ""),

                    "page": None

                })
    # --------------------------------
    # 6. Create embeddings
    # --------------------------------

    print(
        "Creating embeddings..."
    )

    texts = [
        document["text"]
        for document in documents
    ]

    embeddings = create_embeddings(
        texts
    )


    # --------------------------------
    # 7. Store in ChromaDB
    # --------------------------------

    print(
        "Storing vectors in ChromaDB..."
    )

    add_documents(
        documents,
        embeddings
    )


    # --------------------------------
    # 8. Update registry
    # --------------------------------

    for file_path in files_to_process:

        update_registry(
            file_path,
            registry
        )


    # --------------------------------
    # 9. Save registry
    # --------------------------------

    save_registry(
        registry
    )


    print(
        "\nIndexing completed successfully."
    )


# ------------------------------------
# Application entry point
# ------------------------------------

if __name__ == "__main__":

    main()
