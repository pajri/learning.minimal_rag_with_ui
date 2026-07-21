from domain.models.pipeline import RagPipelineContext
from domain.pipeline.base_step import BasePipelineStep

# Default distance threshold applied during filtering.
_DISTANCE_THRESHOLD = 0.5


class ChunkFilteringStep(BasePipelineStep):
    """Filter retrieved chunks by their distance score.

    Chunks whose distance exceeds *distance_threshold* are discarded.
    Surviving chunks are sorted by ascending distance.
    """

    def __init__(self, distance_threshold: float = _DISTANCE_THRESHOLD) -> None:
        self._distance_threshold = distance_threshold

    def handle(self, context: RagPipelineContext) -> None:
        approved_chunks: list = []

        for doc, score in context.documents:
            if score <= self._distance_threshold:
                doc.metadata["distance"] = score
                approved_chunks.append(doc)

        approved_chunks.sort(key=lambda d: d.metadata["distance"])
        context.approved_chunks = approved_chunks

        self._next_handler.handle(context)
