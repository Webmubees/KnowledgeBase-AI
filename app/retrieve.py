from retrieval import retrieve


def main():

    question = input("Ask a question: ")

    results = retrieve(
        question,
        n_results=3
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print("\n===== Retrieved Context =====")

    for index, document in enumerate(documents):

        print(
            f"\n--- Result {index + 1} ---"
        )

        print(
            f"Source: {metadatas[index]['source']}"
        )

        print(
            f"Chunk: {metadatas[index]['chunk']}"
        )

        print(
            f"Distance: {distances[index]}"
        )

        print(
            f"Content:\n{document}"
        )


if __name__ == "__main__":
    main()