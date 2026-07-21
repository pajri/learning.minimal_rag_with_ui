"""Use-case orchestrator for the RAG ask flow.

Runs the pipeline, handles errors, and returns a structured result.
"""

import logging

from application.dto.rag_dto import RagResult
from domain.models.pipeline import RagPipelineContext
from domain.pipeline.base_step import BasePipelineStep

logger = logging.getLogger(__name__)

# Default answer when the pipeline finds no relevant context.
_NO_ANSWER_TEXT = "I do not know the answer based on the provided context."


class RagService:
    """Execute the RAG pipeline for a single question.

    Args:
        pipeline: The first step of a pre-wired Chain-of-Responsibility
            pipeline.  The service creates a fresh :class:`RagPipelineContext`
            for each call.
    """

    def __init__(self, pipeline_head: BasePipelineStep) -> None:
        self._pipeline_head = pipeline_head

    def ask(self, question: str) -> RagResult:
        """Run the full RAG pipeline and return the result."""
        context = RagPipelineContext(query=question)

        self._pipeline_head.handle(context)

        # If a step set an error and there is still no answer, return the
        # error message as the answer.
        if context.error_response is not None:
            logger.warning(
                "Pipeline error in %s: %s",
                context.error_response.pipeline_name,
                context.error_response.error_message,
            )
            return RagResult(
                question=question,
                answer="",
                source_documents=[],
                system_prompt=context.system_prompt,
                user_prompt=context.user_prompt,
            )

        answer = context.answer or _NO_ANSWER_TEXT

        return RagResult(
            question=question,
            answer=answer,
            source_documents=context.documents,
            system_prompt=context.system_prompt,
            user_prompt=context.user_prompt,
        )
