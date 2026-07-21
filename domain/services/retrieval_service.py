"""Pure domain logic for context retrieval operations."""

from langchain_core.documents import Document


def ensure_unique_context(contexts: list[Document]) -> list[Document]:
    """Remove duplicate documents based on stripped page_content."""
    seen: set[str] = set()
    unique: list[Document] = []
    for doc in contexts:
        content = doc.page_content.strip()
        if content not in seen:
            seen.add(content)
            unique.append(doc)
    return unique


def clean_filtered_context(contexts: list[Document]) -> list[Document]:
    """Normalise chunk text (e.g. strip leading '. ') after filtering."""
    for doc in contexts:
        if doc.page_content.startswith(". "):
            doc.page_content = doc.page_content.lstrip(". ")
    return contexts
