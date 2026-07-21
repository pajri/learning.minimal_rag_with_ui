"""DTOs for the content-filtering use case."""

from dataclasses import dataclass
from enum import Enum, auto


class FilterDecision(Enum):
    """What action the caller should take after a filter check."""

    PASS = auto()  # content is safe — proceed
    SAFE_RESPONSE = auto()  # return a canned safe response (e.g. self-help)
    REJECT = auto()  # return a 4xx error to the client


@dataclass
class FilterOutcome:
    """Result of running the input-filtering pipeline."""

    decision: FilterDecision
    filtered_text: str = ""
    reason: str = ""
    safe_message: str = ""  # used when decision == SAFE_RESPONSE


@dataclass
class OutputFilterOutcome:
    """Result of running the output-filtering pipeline."""

    valid: bool
    reason: str = ""
