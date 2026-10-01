from embeddings import create_embeddings
from vector_store import search


def retrieve(
    question,
    n_results=3
):

    query_embedding = create_embeddings(
        [question]
    )[0]

    results = search(
        query_embedding,
        n_results=n_results
    )

    return results