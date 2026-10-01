from retrieval import retrieve
from generation import generate_answer


def answer_question(question):

    results = retrieve(
        question,
        n_results=3
    )

    documents = results["documents"][0]

    context = "\n\n".join(
        documents
    )

    answer = generate_answer(
        question,
        context
    )

    return answer, results