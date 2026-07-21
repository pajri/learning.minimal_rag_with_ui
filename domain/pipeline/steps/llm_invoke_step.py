import logging

from domain.models.pipeline import RagPipelineContext
from domain.pipeline.base_step import BasePipelineStep
from domain.ports.llm_port import LlmPort

logger = logging.getLogger(__name__)


class LlmInvokeStep(BasePipelineStep):
    """Invoke the LLM with the assembled system and user prompts.

    The LLM provider is injected via :class:`LlmPort`, keeping this step
    independent of any specific provider.
    """

    def __init__(self, llm: LlmPort) -> None:
        self._llm = llm

    def handle(self, rag_context: RagPipelineContext) -> None:
        logger.info("Invoking LLM with system + user prompt.")
        answer = self._llm.chat(rag_context.system_prompt, rag_context.user_prompt)
        rag_context.answer = answer
        rag_context.status = "DONE"
