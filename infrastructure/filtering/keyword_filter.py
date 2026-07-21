from domain.ports.content_filter_port import ContentFilterPort, FilterResult

_BLOCKED_KEYWORDS = {"kill", "bomb", "attack"}


class KeywordFilter(ContentFilterPort):
    """Block input containing known unsafe keywords (self-harm, violence, etc.)."""

    def __init__(self, blocked_keywords: set[str] | None = None) -> None:
        self._blocked = blocked_keywords or _BLOCKED_KEYWORDS

    def filter(self, text: str) -> FilterResult:
        lower = text.lower()
        for kw in self._blocked:
            if kw in lower:
                return FilterResult(
                    valid=False,
                    text=text,
                    reason=f"Unsafe content detected: {kw}",
                )
        return FilterResult(valid=True, text=text)

    @property
    def blocked_keywords(self) -> set[str]:
        return set(self._blocked)
