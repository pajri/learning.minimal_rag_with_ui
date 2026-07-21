"""Domain logic for text chunking.

Pure functions — no framework or infrastructure dependencies.
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_docs(documents: list[Document]) -> list[Document]:
    """Split a list of documents into smaller chunks.

    Uses RecursiveCharacterTextSplitter for semantic-aware splitting
    and then assigns unique chunk IDs.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", "? ", "! ", " "],
    )
    chunked_docs = splitter.split_documents(documents)
    chunked_docs = _chunk_id_generator(chunked_docs)
    return chunked_docs


def _chunk_id_generator(chunked_docs: list[Document]) -> list[Document]:
    """Assign unique ``chunk_id`` metadata to every chunk."""
    chunk_counter: dict[str, int] = {}
    for doc in chunked_docs:
        doc_id = doc.metadata["id"]
        if doc_id not in chunk_counter:
            chunk_counter[doc_id] = 0
        chunk_index = chunk_counter[doc_id]
        doc.metadata["chunk_id"] = f"{doc_id}_chunk{chunk_index}"
        chunk_counter[doc_id] += 1
    return chunked_docs
