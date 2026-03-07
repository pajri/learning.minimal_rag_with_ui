from .chunker import chunk_docs
from .store import store_documents

def ingestion_pipeline(documents, collection):
    docs, ids = chunk_docs(documents)
    store_documents(collection, docs, ids)

    return docs

