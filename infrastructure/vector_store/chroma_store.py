import os
import logging

from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

from domain.ports.vector_store_port import VectorStorePort
from infrastructure.config import settings

logger = logging.getLogger(__name__)


class ChromaStore(VectorStorePort):
    """Vector-store adapter backed by ChromaDB."""

    def __init__(
        self,
        collection_name: str,
        embedding_function,
        persist_dir: str | None = None,
    ) -> None:
        persist_dir = persist_dir or settings.chroma_persist_dir
        dir_path = os.path.join(persist_dir, collection_name)
        os.makedirs(dir_path, exist_ok=True)

        self._collection_name = collection_name
        self._chroma = Chroma(
            embedding_function=embedding_function,
            persist_directory=dir_path,
            collection_name=collection_name,
        )
        logger.info(
            "ChromaStore '%s' initialised at %s", collection_name, dir_path
        )

    # -- VectorStorePort -------------------------------------------------------
    def similarity_search_with_score(
        self, query: str, k: int = 3
    ) -> list[tuple[Document, float]]:
        return self._chroma.similarity_search_with_score(query, k=k)

    def add_documents(
        self, documents: list[Document], ids: list[str]
    ) -> None:
        self._chroma.add_documents(documents, ids=ids)

    def delete_all(self) -> None:
        all_ids = self._chroma.get()["ids"]
        if all_ids:
            self._chroma.delete(ids=all_ids)

    def count(self) -> int:
        return self._chroma._collection.count()
