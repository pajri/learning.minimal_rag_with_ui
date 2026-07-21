"""FastAPI dependency-injection wiring.

All "heavy" objects (vector stores, LLM providers, services) are created
once at startup via module-level singletons and exposed through
``Depends()``-compatible factory functions.
"""

import logging

from application.pipeline_factory import create_rag_pipeline
from application.services.filtering_service import FilteringService
from application.services.ingestion_service import IngestionService
from application.services.rag_service import RagService
from domain.ports.llm_port import LlmPort
from domain.ports.vector_store_port import VectorStorePort
from infrastructure.config import settings
from infrastructure.embedding.huggingface_embedding import (
    HuggingFaceEmbeddingProvider,
)
from infrastructure.filtering.composite_filter import CompositeContentFilter
from infrastructure.filtering.injection_detector import InjectionDetector
from infrastructure.filtering.input_validator import InputValidator
from infrastructure.filtering.keyword_filter import KeywordFilter
from infrastructure.filtering.openai_moderation import OpenAIModerationFilter
from infrastructure.filtering.secrets_detector import SecretsDetector
from infrastructure.filtering.text_sanitizer import TextSanitizer
from infrastructure.llm.ollama_provider import OllamaProvider
from infrastructure.llm.openai_provider import OpenAIProvider
from infrastructure.reranker.cross_encoder import CrossEncoderReranker
from infrastructure.vector_store.chroma_store import ChromaStore

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Singleton infrastructure — created once at import time
# ---------------------------------------------------------------------------

_embedding_provider = HuggingFaceEmbeddingProvider(
    model_name=settings.embedding_model,
)

_vectorstore_chunk: VectorStorePort = ChromaStore(
    collection_name="rag_collection",
    embedding_function=_embedding_provider._embeddings,
)

_vectorstore_question: VectorStorePort = ChromaStore(
    collection_name="rag_question",
    embedding_function=_embedding_provider._embeddings,
)

_ollama_llm: LlmPort = OllamaProvider(model=settings.language_model)
_openai_provider = OpenAIProvider()

_reranker = CrossEncoderReranker()

# -- input filter chain ------------------------------------------------------
_input_filter = CompositeContentFilter(
    filters=[
        InputValidator(max_length=1000),
        TextSanitizer(),
        KeywordFilter(),
        OpenAIModerationFilter(openai_provider=_openai_provider),
        InjectionDetector(),
    ]
)

# -- output filter chain -----------------------------------------------------
_output_filter = CompositeContentFilter(
    filters=[
        OpenAIModerationFilter(openai_provider=_openai_provider),
        SecretsDetector(),
    ]
)

# -- services ----------------------------------------------------------------
_filtering_service = FilteringService(
    input_filter=_input_filter,
    output_filter=_output_filter,
)

_rag_pipeline = create_rag_pipeline(
    llm=_ollama_llm,
    reranker=_reranker,
    vectorstore_chunk=_vectorstore_chunk,
    vectorstore_question=_vectorstore_question,
)

_rag_service = RagService(pipeline_head=_rag_pipeline)

_ingestion_service = IngestionService(
    chunk_store=_vectorstore_chunk,
    question_store=_vectorstore_question,
)

# ---------------------------------------------------------------------------
# FastAPI Depends() factories
# ---------------------------------------------------------------------------


def get_vectorstore_chunk() -> VectorStorePort:
    return _vectorstore_chunk


def get_vectorstore_question() -> VectorStorePort:
    return _vectorstore_question


def get_filtering_service() -> FilteringService:
    return _filtering_service


def get_rag_service() -> RagService:
    return _rag_service


def get_ingestion_service() -> IngestionService:
    return _ingestion_service
