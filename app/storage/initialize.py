import chromadb
from app.rag.embeddings import MyEmbeddingFunctionSentenceTransformer

_collection = None

def get_collection():
    global _collection

    if _collection is None:
        client = chromadb.PersistentClient(path="./chroma_db")
        embedding_function = MyEmbeddingFunctionSentenceTransformer()

        _collection = client.get_or_create_collection(
            name="rag_collection",
            embedding_function=embedding_function
        )

    return _collection