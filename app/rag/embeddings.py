from sentence_transformers import SentenceTransformer
from chromadb import Documents, EmbeddingFunction, Embeddings
from app.config import EMBEDDING_MODEL


class MyEmbeddingFunctionSentenceTransformer(EmbeddingFunction):
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = self.model.encode(
            input,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embeddings.tolist()