import logging

import ollama

from domain.ports.llm_port import LlmPort

logger = logging.getLogger(__name__)


class OllamaProvider(LlmPort):
    """LLM adapter for locally-hosted Ollama models."""

    def __init__(self, model: str = "qwen2:0.5b") -> None:
        self._model = model

    def chat(self, system_prompt: str | None, user_prompt: str) -> str:
        logger.info("Calling Ollama model=%s", self._model)
        messages = self._build_messages(system_prompt, user_prompt)
        response = ollama.chat(model=self._model, messages=messages)
        return response["message"]["content"]

    # ------------------------------------------------------------------
    @staticmethod
    def _build_messages(
        system_prompt: str | None, user_prompt: str
    ) -> list[dict[str, str]]:
        if system_prompt is None:
            return [{"role": "user", "content": user_prompt}]
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
