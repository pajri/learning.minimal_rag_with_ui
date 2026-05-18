from application.common.pipeline.base_pipeline_step import BasePipelineStep
from application.config import DISTANCE_THRESHOLD
from application.rag.rag_pipeline_context import RagPipelineContext

class FilteringStep(BasePipelineStep):
    def handle(self, context: RagPipelineContext) :
        approved_chunks = []

        documents = context.documents
        for doc, score in documents:
            if score <= DISTANCE_THRESHOLD:
                doc.metadata["distance"] = score
                approved_chunks.append(doc)
            
        approved_chunks.sort(key=lambda d: d.metadata["distance"])        
        context.approved_chunks = approved_chunks

        self._next_handler.handle(context)


"""
def filter(documents):
    approved_chunks = []
    
    for doc, score in documents:
        if score <= DISTANCE_THRESHOLD:
            doc.metadata["distance"] = score
            approved_chunks.append(doc)
        
    approved_chunks.sort(key=lambda d: d.metadata["distance"])
    
    return approved_chunks
"""