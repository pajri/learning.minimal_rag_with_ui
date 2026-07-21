"""Factory for assembling the RAG Chain-of-Responsibility pipeline.

Wire the concrete steps together with their injected dependencies.
"""

from domain.pipeline.base_step import BasePipelineStep
from domain.pipeline.steps.context_retrieval_step import ContextRetrievalStep
from domain.pipeline.steps.llm_invoke_step import LlmInvokeStep
from domain.pipeline.steps.prompt_building_step import PromptBuildingStep
from domain.pipeline.steps.query_expansion_step import QueryExpansionStep
from domain.pipeline.steps.reranking_step import RerankingStep
from domain.ports.llm_port import LlmPort
from domain.ports.reranker_port import RerankerPort
from domain.ports.vector_store_port import VectorStorePort


def create_rag_pipeline(
    llm: LlmPort,
    reranker: RerankerPort,
    vectorstore_chunk: VectorStorePort,
    vectorstore_question: VectorStorePort,
    *,
    query_expansion_llm: LlmPort | None = None,
) -> BasePipelineStep:
    """Build and wire the default RAG pipeline.

    The pipeline steps (in order):
        1. :class:`QueryExpansionStep` — generate alternative queries
        2. :class:`ContextRetrievalStep` — fetch relevant chunks
        3. :class:`RerankingStep` — re-rank with cross-encoder
        4. :class:`PromptBuildingStep` — assemble system + user prompts
        5. :class:`LlmInvokeStep` — call the LLM

    *query_expansion_llm* defaults to *llm* when not provided, allowing a
    different (e.g. cheaper) model to be used for query expansion.
    """
    expander_llm = query_expansion_llm or llm

    query_expansion = QueryExpansionStep(expander_llm)
    context_retrieval = ContextRetrievalStep(vectorstore_chunk, vectorstore_question)
    reranking = RerankingStep(reranker)
    prompt_building = PromptBuildingStep()
    llm_invoke = LlmInvokeStep(llm)

    query_expansion.set_next(context_retrieval).set_next(reranking).set_next(
        prompt_building
    ).set_next(llm_invoke)

    return query_expansion
