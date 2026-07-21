from domain.ports.content_filter_port import ContentFilterPort, FilterResult
from domain.services.text_cleaner_service import validate_text_length


class InputValidator(ContentFilterPort):
    """Reject empty inputs and inputs exceeding the maximum length."""

    def __init__(self, max_length: int = 1000) -> None:
        self._max_length = max_length

    def filter(self, text: str) -> FilterResult:
        valid, message = validate_text_length(text, self._max_length)
        return FilterResult(valid=valid, text=text, reason="" if valid else message)
