from retrieval import retrieve


def main():

    question = input("Ask a question: ")

    results = retrieve(
        question,
        n_results=3
    )

    if results is None:
        print(
            "\nI don't have enough information "
            "in the knowledge base."
        )
        return

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print("\n===== Retrieved Context =====")

    for index, document in enumerate(documents):

        metadata = metadatas[index]

        print(
            f"\n--- Result {index + 1} ---"
        )

        print(
            f"Source: {metadata.get('source', 'unknown')}"
        )

        print(
            f"Chunk: {metadata.get('chunk', 'unknown')}"
        )

        print(
            f"Page: {metadata.get('page', 'N/A')}"
        )

        print(
            f"Type: {metadata.get('document_type', 'unknown')}"
        )

        print(
            f"Distance: {distances[index]}"
        )

        print(
            f"Content:\n{document}"
        )


if __name__ == "__main__":
    main()