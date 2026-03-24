import logging
from .chunker import chunk_docs

logger = logging.getLogger(__name__)

def chunk_ingestion_pipeline(vectorstore, doc_source):
    logger.info("starting ingestion pipeline")

    chunked_docs = chunk_docs(doc_source)
    print(f"doc_source size: {len(doc_source)}; chunked_docs size: {len(chunked_docs)}")

    vectorstore.add_documents(chunked_docs, ids=[doc.metadata["chunk_id"] for doc in chunked_docs])
    print(f"collection size: {vectorstore._collection.count()}")

    logger.info("done ingestion pipeline")
    return chunked_docs


def question_ingestion_pipeline(vectorstore, doc_question):
    logger.info("starting question ingestion pipeline")

    print(f"doc_question size: {len(doc_question)}")

    vectorstore.add_documents(doc_question, ids=[doc.metadata["id"] for doc in doc_question])

    print(f"collection size: {vectorstore._collection.count()}")

    logger.info("done question ingestion pipeline")
    return doc_question
