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

    for document in documents:

        source = document["source"]
        chunk = document["chunk"]
        page = document.get("page")

        # --------------------------------
        # Create unique ID
        # --------------------------------

        if page is not None:

            document_id = (
                f"{source}_page{page}_chunk{chunk}"
            )

        else:

            document_id = (
                f"{source}_chunk{chunk}"
            )

        ids.append(document_id)

        # --------------------------------
        # Store text
        # --------------------------------

        texts.append(
            document["text"]
        )

        # --------------------------------
        # Store metadata
        # --------------------------------

        metadata = {
            "source": source,
            "chunk": chunk,
            "document_type": document["document_type"]
        }

        if page is not None:

            metadata["page"] = page

        metadatas.append(
            metadata
        )

    # --------------------------------
    # Store in ChromaDB
    # --------------------------------

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


def delete_document(source):

    results = collection.get(
        where={
            "source": source
        }
    )

    ids = results["ids"]

    if ids:

        collection.delete(
            ids=ids
        )