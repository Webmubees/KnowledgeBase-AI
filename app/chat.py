from rag import answer_question


def main():

    question = input("Ask a question: ")

    answer, results = answer_question(
        question
    )

    print("\n===== Answer =====")
    print(answer)

    if results is None:
        return

    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print("\n===== Sources =====")

    for index, metadata in enumerate(metadatas):

        source = metadata.get(
            "source",
            "unknown"
        )

        chunk = metadata.get(
            "chunk",
            "unknown"
        )

        page = metadata.get(
            "page",
            None
        )

        document_type = metadata.get(
            "document_type",
            "unknown"
        )

        if page is not None:
            location = f"page {page}, chunk {chunk}"
        else:
            location = f"chunk {chunk}"

        print(
            f"\n[{index + 1}] {source}"
        )

        print(
            f"    Type: {document_type}"
        )

        print(
            f"    Location: {location}"
        )

        print(
            f"    Distance: {distances[index]:.4f}"
        )


if __name__ == "__main__":
    main()