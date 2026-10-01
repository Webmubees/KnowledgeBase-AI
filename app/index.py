from pathlib import Path

from ingestion import load_document
from embeddings import create_embeddings

from vector_store import (
    add_documents,
    delete_document
)

from document_registry import (
    load_registry,
    save_registry,
    is_document_changed
)


DOCUMENTS_DIR = Path(
    "data/documents"
)


def main():

    registry = load_registry()

    documents_to_index = []

    # --------------------------------
    # Find deleted documents
    # --------------------------------

    current_files = {
        file_path.name
        for file_path in DOCUMENTS_DIR.iterdir()
        if file_path.is_file()
    }

    registered_files = set(
        registry.keys()
    )

    deleted_files = (
        registered_files - current_files
    )

    for filename in deleted_files:

        print(
            f"DELETE: {filename}"
        )

        delete_document(
            filename
        )

        del registry[filename]

    # --------------------------------
    # Find new / changed documents
    # --------------------------------

    for file_path in DOCUMENTS_DIR.iterdir():

        if not file_path.is_file():
            continue

        changed, file_hash = (
            is_document_changed(
                file_path,
                registry
            )
        )

        if not changed:

            print(
                f"SKIP: {file_path.name}"
            )

            continue

        print(
            f"INDEX: {file_path.name}"
        )

        # Remove old chunks first.
        # This is important when a document
        # changes and the new version has
        # fewer chunks than the old version.

        delete_document(
            file_path.name
        )

        documents_to_index.append(
            (
                file_path,
                file_hash
            )
        )

    # --------------------------------
    # Nothing changed
    # --------------------------------

    if not documents_to_index:

        save_registry(
            registry
        )

        print(
            "\nNo documents need indexing."
        )

        return

    all_documents = []

    # --------------------------------
    # Load and chunk
    # --------------------------------

    for file_path, file_hash in (
        documents_to_index
    ):

        documents = load_document(
            file_path
        )

        all_documents.extend(
            documents
        )

        registry[file_path.name] = {
            "hash": file_hash,

            "chunks": len(documents),

            "document_type":
                file_path.suffix.lower().replace(
                    ".",
                    ""
                )
        }

    print(
        f"\nLoaded {len(all_documents)} chunks"
    )

    # --------------------------------
    # Create embeddings
    # --------------------------------

    print(
        "Creating embeddings..."
    )

    texts = [
        document["text"]
        for document in all_documents
    ]

    embeddings = create_embeddings(
        texts
    )

    # --------------------------------
    # Store vectors
    # --------------------------------

    print(
        "Storing vectors in ChromaDB..."
    )

    add_documents(
        all_documents,
        embeddings
    )

    # --------------------------------
    # Save registry
    # --------------------------------

    save_registry(
        registry
    )

    print(
        "Indexing completed successfully."
    )


if __name__ == "__main__":
    main()