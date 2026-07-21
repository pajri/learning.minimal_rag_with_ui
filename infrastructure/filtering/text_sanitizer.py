from domain.ports.content_filter_port import ContentFilterPort, FilterResult
from domain.services.text_cleaner_service import sanitize_text


class TextSanitizer(ContentFilterPort):
    """Non-blocking filter that normalises whitespace and strips HTML tags."""

    def filter(self, text: str) -> FilterResult:
        cleaned = sanitize_text(text)
        return FilterResult(valid=True, text=cleaned)
