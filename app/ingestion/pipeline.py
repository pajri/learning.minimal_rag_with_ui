from .chunker import chunk_docs
from .store import store_documents

def ingestion_pipeline(documents):
    docs, ids = chunk_docs(documents)
    store_documents(docs, ids)

    return docs

