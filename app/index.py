from ingestion import load_documents
from embeddings import create_embeddings
from vector_store import add_documents


def main():

    print("Loading documents...")

    documents = load_documents()

    print(
        f"Loaded {len(documents)} chunks"
    )

    print("Creating embeddings...")

    texts = [
        document["text"]
        for document in documents
    ]

    embeddings = create_embeddings(
        texts
    )

    print("Storing vectors in ChromaDB...")

    add_documents(
        documents,
        embeddings
    )

    print("Indexing completed successfully.")


if __name__ == "__main__":
    main()