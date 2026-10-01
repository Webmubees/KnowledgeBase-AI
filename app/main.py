from ingestion import load_documents


def main():

    documents = load_documents()

    print(
        f"Created {len(documents)} chunk(s)"
    )

    for document in documents:

        print("\n--------------------")

        print(
            f"Source: {document['source']}"
        )

        print(
            f"Chunk: {document['chunk']}"
        )

        print(
            f"Text: {document['text']}"
        )


if __name__ == "__main__":
    main()