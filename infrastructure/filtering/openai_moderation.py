import logging

from domain.ports.content_filter_port import ContentFilterPort, FilterResult
from infrastructure.llm.openai_provider import OpenAIProvider

logger = logging.getLogger(__name__)


class OpenAIModerationFilter(ContentFilterPort):
    """Delegate content-moderation checks to the OpenAI Moderation API."""

    def __init__(self, openai_provider: OpenAIProvider | None = None) -> None:
        self._provider = openai_provider or OpenAIProvider()

    def filter(self, text: str) -> FilterResult:
        response = self._provider.moderate_text(text)
        if not response.results[0].flagged:
            return FilterResult(valid=True, text=text)

        logger.info("OpenAI moderation flagged input: %s", response)
        categories = response.results[0].categories.model_dump()
        flagged = [cat for cat, is_flagged in categories.items() if is_flagged]
        return FilterResult(
            valid=False,
            text=text,
            reason=f"Unsafe content detected by moderation: {', '.join(flagged)}",
        )
