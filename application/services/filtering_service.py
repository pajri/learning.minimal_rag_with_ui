"""Use-case orchestrator for content filtering.

Decides what HTTP-level action to take based on filter results,
consolidating the logic that was previously scattered across ``routes.py``.
"""

import logging

from application.dto.filtering_dto import FilterDecision, FilterOutcome, OutputFilterOutcome
from domain.ports.content_filter_port import ContentFilterPort

logger = logging.getLogger(__name__)

# Safe canned responses for specific rejection reasons.
_SAFE_RESPONSES: dict[str, str] = {
    "self-harm": (
        "I'm sorry to hear that you're feeling this way. "
        "It might be helpful to talk to someone you trust about how you're "
        "feeling, such as a close friend, family member, or mental health "
        "professional. Remember that you're not alone, and there are people "
        "who care about you and want to support you."
    ),
}

_DEFAULT_SAFE_RESPONSE = "I'm unable to provide a response to that request."


class FilteringService:
    """Orchestrate input and output content filtering.

    Args:
        input_filter: Composite (or single) :class:`ContentFilterPort`
            applied to user questions before the RAG pipeline.
        output_filter: :class:`ContentFilterPort` applied to the LLM answer.
    """

    def __init__(
        self,
        input_filter: ContentFilterPort,
        output_filter: ContentFilterPort,
    ) -> None:
        self._input_filter = input_filter
        self._output_filter = output_filter

    # ------------------------------------------------------------------
    # Input filtering
    # ------------------------------------------------------------------
    def check_input(self, question: str) -> FilterOutcome:
        """Run input filtering and return a structured decision."""
        logger.info("Running input filtering on: %s", question[:80])
        result = self._input_filter.filter(question)

        if result.valid:
            return FilterOutcome(
                decision=FilterDecision.PASS,
                filtered_text=result.text,
            )

        # Some rejection reasons should produce a safe canned response
        # instead of a 4xx error (e.g. self-harm).
        for trigger, safe_msg in _SAFE_RESPONSES.items():
            if trigger in result.reason.lower():
                return FilterOutcome(
                    decision=FilterDecision.SAFE_RESPONSE,
                    filtered_text=result.text,
                    reason=result.reason,
                    safe_message=safe_msg,
                )
        return FilterOutcome(
            decision=FilterDecision.REJECT,
            filtered_text=result.text,
            reason=result.reason,
        )

    # ------------------------------------------------------------------
    # Output filtering
    # ------------------------------------------------------------------
    def check_output(self, answer: str, contexts: list) -> OutputFilterOutcome:
        """Run output filtering on the LLM answer."""
        result = self._output_filter.filter(answer)
        if not result.valid:
            return OutputFilterOutcome(
                valid=False,
                reason=result.reason,
            )
        return OutputFilterOutcome(valid=True)
