def retrieve(collection, question, k=5):
    results = collection.query(
        query_texts=[question],
        n_results=k
    )

    return results

