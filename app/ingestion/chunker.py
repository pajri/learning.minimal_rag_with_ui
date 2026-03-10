import logging

logger = logging.getLogger(__name__)

def chunk_docs(documents):
    for doc in documents:
        doc.content = doc.content.strip()[:100]

    return documents