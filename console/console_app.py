"""Console-based driver for the RAG pipeline.

Uses the same application services as the FastAPI adapter, wired manually
(without FastAPI's DI system).
"""

import json
import logging
import sys
from pathlib import Path

# Ensure the project root is on sys.path.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from application.pipeline_factory import create_rag_pipeline
from application.services.rag_service import RagService
from infrastructure.config import settings
from infrastructure.embedding.huggingface_embedding import (
    HuggingFaceEmbeddingProvider,
)
from infrastructure.llm.ollama_provider import OllamaProvider
from infrastructure.reranker.cross_encoder import CrossEncoderReranker
from infrastructure.vector_store.chroma_store import ChromaStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    # -- wire up infrastructure -----------------------------------------------
    embedding = HuggingFaceEmbeddingProvider(model_name=settings.embedding_model)

    chunk_store = ChromaStore(
        collection_name="rag_collection",
        embedding_function=embedding._embeddings,
    )
    question_store = ChromaStore(
        collection_name="rag_question",
        embedding_function=embedding._embeddings,
    )

    llm = OllamaProvider(model=settings.language_model)
    reranker = CrossEncoderReranker()

    pipeline = create_rag_pipeline(
        llm=llm,
        reranker=reranker,
        vectorstore_chunk=chunk_store,
        vectorstore_question=question_store,
    )
    rag_service = RagService(pipeline_head=pipeline)

    # -- interactive loop -----------------------------------------------------
    print("RAG Console — type a question (or 'quit')")
    while True:
        try:
            q = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if q.lower() in ("quit", "exit", "q"):
            break
        if not q:
            continue

        result = rag_service.ask(q)
        print(f"\nAnswer: {result.answer}")
        if result.source_documents:
            print(f"\nSources ({len(result.source_documents)}):")
            for i, doc in enumerate(result.source_documents, 1):
                print(f"  [{i}] {doc.page_content[:120]}…")


if __name__ == "__main__":
    main()
