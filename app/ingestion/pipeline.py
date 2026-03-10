import logging
from .chunker import chunk_docs
from .store import store_documents

logger = logging.getLogger(__name__)

def ingestion_pipeline(documents, collection):
    logger.info("starting ingestion pipeline")

    docs = chunk_docs(documents)

    store_documents(collection, docs)

    logger.info("done ingestion pipeline")
    return docs

