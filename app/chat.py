from rag import answer_question


def main():

    question = input(
        "Ask a question: "
    )

    answer, results = answer_question(
        question
    )

    print("\n===== Answer =====")

    print(answer)

    print("\n===== Sources =====")

    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for index, metadata in enumerate(
        metadatas
    ):

        print(
            f"{index + 1}. "
            f"{metadata['source']} "
            f"(chunk {metadata['chunk']}) "
            f"[distance: {distances[index]:.4f}]"
        )


if __name__ == "__main__":
    main()