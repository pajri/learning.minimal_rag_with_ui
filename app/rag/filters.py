from app.config import DISTANCE_THRESHOLD

def filter(documents):
    approved_chunks = []
    
    for doc, score in documents:
        if score <= DISTANCE_THRESHOLD:
            doc.metadata["distance"] = score
            approved_chunks.append(doc)
        
    approved_chunks.sort(key=lambda d: d.metadata["distance"])
    
    return approved_chunks