import chromadb
from app.config import DISTANCE_THRESHOLD
from .embeddings import MyEmbeddingFunctionSentenceTransformer
from app.storage.initialize import get_collection

def retrieve(question, k=5):
    collection = get_collection()
    results = collection.query(
        query_texts=[question],
        n_results=k
    )

    return results

