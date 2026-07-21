from abc import ABC, abstractmethod

from langchain_core.documents import Document


class RerankerPort(ABC):
    """Abstract port for cross-encoder reranking.

    Rerankers re-score retrieved documents against the query to improve
    the order of context chunks before they are passed to the LLM.
    """

    @abstractmethod
    def rerank(
        self, query: str, documents: list[Document]
    ) -> list[Document]:
        """Return documents re-sorted by relevance to *query*."""
        ...
