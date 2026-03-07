def chunk_docs(documents):
    docs = [doc.strip()[:100] for doc in documents]
    ids = [f"doc_{i}" for i in range(len(docs))]

    return docs, ids