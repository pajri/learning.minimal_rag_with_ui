from sentence_transformers import CrossEncoder

from application.common.pipeline.base_pipeline_step import BasePipelineStep
from application.rag.rag_pipeline_context import RagPipelineContext

class RerankingStep(BasePipelineStep):
    reranker =  CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    
    def handle(self, context: RagPipelineContext):
        query = context.query
        documents = context.documents

        pairs = [(query, doc.page_content) for doc in documents]
        scores = self.reranker.predict(pairs)

        ranked_docs = sorted(
            zip(documents, scores),
            key = lambda x: x[1],
            reverse=True
        )

        context.documents = [doc for doc, _ in ranked_docs]
        self._next_handler.handle(context)
    

"""
reranker =  CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
def rerank(query, documents):
    pairs = [(query, doc.page_content) for doc in documents]
    scores = reranker.predict(pairs)

    ranked_docs = sorted(
        zip(documents, scores),
        key = lambda x: x[1],
        reverse=True
    )

    return [doc for doc, _ in ranked_docs]
"""