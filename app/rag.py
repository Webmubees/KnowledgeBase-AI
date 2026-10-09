
from .retrieval import retrieve
from .generation import generate_answer


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

    if not documents:
        return (
            "I don't have enough information "
            "in the knowledge base to answer "
            "this question.",
            None
        )

    # Build the context from document text only.
    # Source metadata is returned separately for citations.
    context_parts = []

    for document in documents:
        if document and document.strip():
            context_parts.append(document.strip())

    if not context_parts:
        return (
            "I don't have enough information "
            "in the knowledge base to answer "
            "this question.",
            None
        )

    context = "\n\n".join(context_parts)

    answer = generate_answer(
        question,
        context
    )

    return answer, results
