from retrieval import retrieve
from generation import generate_answer


def answer_question(question):

    results = retrieve(
        question,
        n_results=3
    )

    if results is None:

        return (
            "I don't have enough information "
            "in the knowledge base to answer "
            "this question.",
            None
        )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []

    for index, (
        document,
        metadata
    ) in enumerate(
        zip(
            documents,
            metadatas
        ),
        start=1
    ):

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

        if page is not None and page != -1:

            location = (
                f"{source}, "
                f"page {page}, "
                f"chunk {chunk}"
            )

        else:

            location = (
                f"{source}, "
                f"chunk {chunk}"
            )

        context_parts.append(
            f"[Source {index}: {location}]\n"
            f"{document}"
        )

    context = "\n\n".join(
        context_parts
    )

    answer = generate_answer(
        question,
        context
    )

    return answer, results