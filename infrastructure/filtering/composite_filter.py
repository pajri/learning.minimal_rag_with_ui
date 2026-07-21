"""Composite pattern: chain multiple ContentFilterPort implementations."""

from domain.ports.content_filter_port import ContentFilterPort, FilterResult


class CompositeContentFilter(ContentFilterPort):
    """Run a sequence of :class:`ContentFilterPort` checks.

    Each filter in the chain gets the (possibly sanitised) output of the
    previous one.  The first rejection short-circuits the remaining checks.
    """

    def __init__(self, filters: list[ContentFilterPort]) -> None:
        if not filters:
            raise ValueError("At least one filter is required.")
        self._filters = filters

    def filter(self, text: str) -> FilterResult:
        current = text
        for f in self._filters:
            result = f.filter(current)
            if not result.valid:
                return result
            current = result.text  # carry forward sanitised text
        return FilterResult(valid=True, text=current)
