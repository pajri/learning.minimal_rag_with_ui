from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

from domain.ports.reranker_port import RerankerPort


class CrossEncoderReranker(RerankerPort):
    """Cross-encoder reranker using sentence-transformers.

    Loads a pre-trained cross-encoder model and re-scores
    documents against the query.
    """

    def __init__(
        self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    ) -> None:
        self._model_name = model_name
        self._model = CrossEncoder(model_name)

    def rerank(
        self, query: str, documents: list[Document]
    ) -> list[Document]:
        if not documents:
            return []

        pairs = [(query, doc.page_content) for doc in documents]
        scores = self._model.predict(pairs)

        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True,
        )
        return [doc for doc, _ in ranked]
