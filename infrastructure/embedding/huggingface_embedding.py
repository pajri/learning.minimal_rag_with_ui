from langchain_huggingface import HuggingFaceEmbeddings

from domain.ports.embedding_port import EmbeddingPort


class HuggingFaceEmbeddingProvider(EmbeddingPort):
    """Embedding adapter wrapping a HuggingFace sentence-transformer model."""

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5") -> None:
        self._model_name = model_name
        self._embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            encode_kwargs={"normalize_embeddings": True},
        )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embeddings.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        return self._embeddings.embed_query(text)
