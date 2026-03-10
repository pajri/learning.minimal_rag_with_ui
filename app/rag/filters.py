from app.config import DISTANCE_THRESHOLD

def filter(documents):
    approved_chunks = []
    retrieval_log = []

    for doc in documents:
        retrieval_log.append({
            "document": doc.id,
            "distance": doc.distance
        })

        if doc.distance <= DISTANCE_THRESHOLD:
            approved_chunks.append(doc)

    return approved_chunks, retrieval_log, len(approved_chunks) > 0