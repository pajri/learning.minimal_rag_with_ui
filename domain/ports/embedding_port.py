from abc import ABC, abstractmethod


class EmbeddingPort(ABC):
    """Abstract port for text-embedding providers.

    Implementations (e.g. HuggingFace, OpenAI embeddings) convert text
    into vector representations used for semantic search.
    """

    @abstractmethod
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of documents into vectors."""
        ...

    @abstractmethod
    def embed_query(self, text: str) -> list[float]:
        """Embed a single query text into a vector."""
        ...
