from embeddings import create_embeddings
from vector_store import search


RELEVANCE_THRESHOLD = 1.2


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

    distances = results["distances"][0]

    if not distances:
        return None

    best_distance = distances[0]

    if best_distance > RELEVANCE_THRESHOLD:
        return None

    return results