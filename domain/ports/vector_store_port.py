from abc import ABC, abstractmethod

from langchain_core.documents import Document


class VectorStorePort(ABC):
    """Abstract port for vector-store operations.

    Implementations (e.g. ChromaDB) handle embedding-based similarity search,
    document insertion, and collection management.
    """

    @abstractmethod
    def similarity_search_with_score(
        self, query: str, k: int = 3
    ) -> list[tuple[Document, float]]:
        """Return the k most similar documents with their distance scores."""
        ...

    @abstractmethod
    def add_documents(
        self, documents: list[Document], ids: list[str]
    ) -> None:
        """Add documents to the vector store."""
        ...

    @abstractmethod
    def delete_all(self) -> None:
        """Remove all documents from the collection."""
        ...

    @abstractmethod
    def count(self) -> int:
        """Return the number of documents in the collection."""
        ...
