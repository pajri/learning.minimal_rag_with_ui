from app.config import DISTANCE_THRESHOLD

def filter(documents, distances):
    approved_chunks = []
    retrieval_log = []

    for doc, dist in zip(documents, distances):
        retrieval_log.append({
            "document": doc,
            "distance": dist
        })

        if dist <= DISTANCE_THRESHOLD:
            approved_chunks.append(doc)

    return approved_chunks, retrieval_log, len(approved_chunks) > 0