from domain.models.pipeline import RagPipelineContext
from domain.pipeline.base_step import BasePipelineStep
from domain.services.prompt_service import build_system_prompt, build_user_prompt


class PromptBuildingStep(BasePipelineStep):
    """Assemble system and user prompts from retrieved context chunks.

    This step is pure string assembly — it has no external dependencies.
    """

    def handle(self, rag_context: RagPipelineContext) -> None:
        rag_context.system_prompt = build_system_prompt()
        rag_context.user_prompt = build_user_prompt(
            rag_context.documents, rag_context.query
        )
        self._next_handler.handle(rag_context)
