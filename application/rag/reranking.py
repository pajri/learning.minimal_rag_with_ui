from sentence_transformers import CrossEncoder

reranker =  CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query, documents):
    pairs = [(query, doc.page_content) for doc in documents]
    scores = reranker.predict(pairs)

    ranked_docs = sorted(
        zip(documents, scores),
        key = lambda x: x[1],
        reverse=True
    )

    return [doc for doc, _ in ranked_docs]

