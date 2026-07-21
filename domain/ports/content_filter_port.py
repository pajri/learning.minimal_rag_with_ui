from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class FilterResult:
    """Outcome of a content-filter check."""

    valid: bool
    text: str  # possibly sanitised / cleaned text
    reason: str = ""  # reason for rejection (empty when valid)


class ContentFilterPort(ABC):
    """Abstract port for content-safety filtering.

    Each implementation checks a specific dimension (keywords,
    injection, OpenAI moderation, etc.).  Use CompositeContentFilter
    to chain several together.
    """

    @abstractmethod
    def filter(self, text: str) -> FilterResult:
        """Check *text* and return a FilterResult."""
        ...
