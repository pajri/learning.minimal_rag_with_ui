import re

from domain.ports.content_filter_port import ContentFilterPort, FilterResult

# Matches OpenAI-style API keys (sk-...).
_API_KEY_PATTERN = re.compile(r"sk-\w+")


class SecretsDetector(ContentFilterPort):
    """Scan output text for leaked API keys or other secrets."""

    def filter(self, text: str) -> FilterResult:
        if _API_KEY_PATTERN.search(text):
            return FilterResult(
                valid=False,
                text=text,
                reason="Sensitive data detected in output.",
            )
        return FilterResult(valid=True, text=text)
