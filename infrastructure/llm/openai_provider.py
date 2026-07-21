from openai import OpenAI

from domain.ports.llm_port import LlmPort
from infrastructure.config import settings


class OpenAIProvider(LlmPort):
    """LLM adapter for the OpenAI API.

    Also exposes a moderation helper used by the content-filtering adapters.
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: str | None = None,
    ) -> None:
        self._model = model
        self._client = OpenAI(api_key=api_key or settings.openai_api_key)

    # -- LlmPort ---------------------------------------------------------------
    def chat(self, system_prompt: str | None, user_prompt: str) -> str:
        messages = self._build_messages(system_prompt, user_prompt)
        response = self._client.chat.completions.create(
            model=self._model, messages=messages, temperature=0
        )
        return response.choices[0].message.content.strip()

    # -- Moderation (used by filtering adapters) -------------------------------
    def moderate_text(self, text: str):
        """Run OpenAI moderation API on *text*."""
        return self._client.moderations.create(
            model="omni-moderation-latest", input=text
        )

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
