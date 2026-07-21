import json
import logging
import re

from domain.models.pipeline import RagPipelineContext
from domain.pipeline.base_step import BasePipelineStep
from domain.ports.llm_port import LlmPort

logger = logging.getLogger(__name__)


class QueryExpansionStep(BasePipelineStep):
    """Expand the user's original query into multiple alternative search queries.

    Uses an LLM (injected via :class:`LlmPort`) to generate variants,
    then appends the original query to the list.
    """

    def __init__(self, llm: LlmPort) -> None:
        self._llm = llm

    def handle(self, context: RagPipelineContext) -> None:
        model = context.model
        query = context.query

        prompt = f"""Generate 3 alternative search queries.

Rules:
- Return ONLY a list like this: ["q1", "q2", "q3"]
- No explanation
- No numbering
- No extra text

Query: "{query}"
"""
        response = self._llm.chat(None, prompt)
        logger.info("Query expansion response: %s", response)

        expanded_queries = self._extract_queries(response)
        logger.info("Expanded queries: %s", expanded_queries)

        expanded_queries.append(query)
        context.expanded_queries = expanded_queries

        self._next_handler.handle(context)

    # ------------------------------------------------------------------
    def _extract_queries(self, text: str) -> list[str]:
        """Robustly extract query strings from LLM output."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        # Last-resort fallback: split on newlines
        queries: list[str] = []
        for line in text.split("\n"):
            line = line.strip("-•1234567890. ").strip()
            if len(line) > 5:
                queries.append(line)
        return queries
