from ingestion import load_documents
from embeddings import create_embeddings


def main():

    documents = load_documents()

    texts = [
        document["text"]
        for document in documents
    ]

    embeddings = create_embeddings(texts)

    print(
        f"Created {len(embeddings)} embedding(s)"
    )

    for index, embedding in enumerate(embeddings):

        print("\n--------------------")

        print(
            f"Chunk: {index}"
        )

        print(
            f"Vector size: {len(embedding)}"
        )

        print(
            f"First 5 values: {embedding[:5]}"
        )


if __name__ == "__main__":
    main()