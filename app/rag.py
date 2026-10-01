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

    for document, metadata in zip(
        documents,
        metadatas
    ):

        context_parts.append(
            document
        )

    context = "\n\n".join(
        context_parts
    )

    answer = generate_answer(
        question,
        context
    )

    return answer, results