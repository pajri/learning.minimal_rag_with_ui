from openai import OpenAI

from domain.ports.llm_port import LlmPort
from infrastructure.config import settings


class DeepSeekProvider(LlmPort):
    """LLM adapter for the DeepSeek API (OpenAI-compatible endpoint)."""

    def __init__(
        self,
        model: str = "deepseek-chat",
        api_key: str | None = None,
    ) -> None:
        self._model = model
        self._client = OpenAI(
            api_key=api_key or settings.deepseek_api_key,
            base_url="https://api.deepseek.com",
        )

    def chat(self, system_prompt: str | None, user_prompt: str) -> str:
        messages = self._build_messages(system_prompt, user_prompt)
        response = self._client.chat.completions.create(
            model=self._model, messages=messages, temperature=0
        )
        return response.choices[0].message.content

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
