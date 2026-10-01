import chromadb


CHROMA_PATH = "chroma_db"

COLLECTION_NAME = "knowledge"


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


def add_documents(
    documents,
    embeddings
):

    ids = []

    texts = []

    metadatas = []

    for index, document in enumerate(documents):

        ids.append(
            f"{document['source']}_{document['chunk']}"
        )

        texts.append(
            document["text"]
        )

        metadatas.append(
            {
                "source": document["source"],
                "chunk": document["chunk"]
            }
        )

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )


def search(
    query_embedding,
    n_results=3
):

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=n_results
    )

    return results