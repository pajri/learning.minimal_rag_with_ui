import logging
import ollama

from application.common.pipeline.base_pipeline_step import BasePipelineStep
from application.config import LANGUAGE_MODEL
from application.rag.rag_pipeline_context import RagPipelineContext


class LlmPipelineStep(BasePipelineStep):
    def handle(self, rag_context: RagPipelineContext):
        logger = logging.getLogger(__name__)
        system_prompt = rag_context.system_prompt
        user_prompt = rag_context.user_prompt

        logger.info(f"using language model: {LANGUAGE_MODEL}")
        messages = self.create_message(system_prompt, user_prompt)

        response = ollama.chat(
            model=LANGUAGE_MODEL,
            messages=messages,
        )

        rag_context.answer = response["message"]["content"]
        rag_context.status = "DONE"
    
    def create_message(self, system_prompt, user_prompt):
        if system_prompt is None:
            return [{"role": "user", "content": user_prompt}]

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]