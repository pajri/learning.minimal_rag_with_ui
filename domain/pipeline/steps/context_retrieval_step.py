import logging

from domain.models.pipeline import RagPipelineContext, RagPipelineErrorResponse
from domain.pipeline.base_step import BasePipelineStep
from domain.ports.vector_store_port import VectorStorePort
from domain.services.retrieval_service import (
    clean_filtered_context,
    ensure_unique_context,
)

logger = logging.getLogger(__name__)

# Distance threshold used when fetching chunks by similarity.
_DISTANCE_THRESHOLD = 0.5


class ContextRetrievalStep(BasePipelineStep):
    """Retrieve relevant document chunks from the vector store.

    For each expanded query, performs a similarity search, deduplicates
    results, and stores them on the pipeline context.
    """

    def __init__(
        self,
        vectorstore_chunk: VectorStorePort,
        vectorstore_question: VectorStorePort,
        distance_threshold: float = _DISTANCE_THRESHOLD,
    ) -> None:
        self._vectorstore_chunk = vectorstore_chunk
        self._vectorstore_question = vectorstore_question
        self._distance_threshold = distance_threshold

    # ------------------------------------------------------------------
    def handle(self, rag_context: RagPipelineContext) -> None:
        expanded_queries = rag_context.expanded_queries

        # Collect chunks by similarity search for each expanded query.
        context_results: list = []
        for q in expanded_queries:
            results = self._get_context_by_query(q)
            context_results.extend(results)

        logger.info("Retrieved %d context chunks total.", len(context_results))

        # Deduplicate.
        contexts = ensure_unique_context(context_results)
        logger.info("Unique context chunks: %d", len(contexts))

        # Short-circuit when nothing was found.
        if len(contexts) == 0:
            rag_context.status = "error"
            rag_context.error_response = RagPipelineErrorResponse(
                pipeline_name="ContextRetrievalStep",
                error_message="No relevant context found for the question.",
            )
            return

        # Normalise chunk text.
        contexts = clean_filtered_context(contexts)
        rag_context.documents = contexts

        self._next_handler.handle(rag_context)

    # ------------------------------------------------------------------
    def _get_context_by_query(self, query: str) -> list:
        """Return filtered chunks for a single query."""
        raw = self._vectorstore_chunk.similarity_search_with_score(query, k=3)
        return self._filter_by_distance(raw)

    def _filter_by_distance(
        self, docs_with_scores: list
    ) -> list:
        approved: list = []
        for doc, score in docs_with_scores:
            if score <= self._distance_threshold:
                doc.metadata["distance"] = score
                approved.append(doc)
        approved.sort(key=lambda d: d.metadata["distance"])
        return approved
