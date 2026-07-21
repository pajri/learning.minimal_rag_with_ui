from domain.models.pipeline import RagPipelineContext
from domain.pipeline.base_step import BasePipelineStep
from domain.ports.reranker_port import RerankerPort


class RerankingStep(BasePipelineStep):
    """Re-rank retrieved documents using a cross-encoder model.

    The step delegates to a :class:`RerankerPort` implementation so the
    domain layer does not depend on a specific model or library.
    """

    def __init__(self, reranker: RerankerPort) -> None:
        self._reranker = reranker

    def handle(self, context: RagPipelineContext) -> None:
        query = context.query
        documents = context.documents

        ranked = self._reranker.rerank(query, documents)
        context.documents = ranked

        self._next_handler.handle(context)
