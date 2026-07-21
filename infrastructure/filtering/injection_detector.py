from domain.ports.content_filter_port import ContentFilterPort, FilterResult

_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "act as system",
    "reveal the system prompt",
    "you are now",
]


class InjectionDetector(ContentFilterPort):
    """Detect common prompt-injection patterns in user input."""

    def __init__(self, patterns: list[str] | None = None) -> None:
        self._patterns = patterns or _INJECTION_PATTERNS

    def filter(self, text: str) -> FilterResult:
        lower = text.lower()
        for pattern in self._patterns:
            if pattern in lower:
                return FilterResult(
                    valid=False,
                    text=text,
                    reason="Potential prompt injection detected.",
                )
        return FilterResult(valid=True, text=text)
