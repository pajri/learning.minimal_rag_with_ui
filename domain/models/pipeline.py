from __future__ import annotations

from dataclasses import dataclass, field

from langchain_core.documents import Document


class PipelineContext:
    """Base context passed along pipeline steps."""

    pass


@dataclass
class RagPipelineErrorResponse:
    """Captures an error that occurred inside a pipeline step."""

    pipeline_name: str = ""
    error_message: str = ""


@dataclass
class RagPipelineContext(PipelineContext):
    """Context object that flows through the RAG pipeline steps.

    Each step reads from and writes to this context, avoiding the need
    for return-value plumbing through the Chain of Responsibility.
    """

    query: str = ""
    model: str = "deepseek-r1:1.5b"
    expanded_queries: list[str] = field(default_factory=list)

    vectorstore_chunk: object = None
    vectorstore_question: object = None

    documents: list[Document] = field(default_factory=list)
    approved_chunks: list[Document] = field(default_factory=list)

    system_prompt: str = ""
    user_prompt: str = ""
    answer: str = ""

    status: str = ""
    error_response: RagPipelineErrorResponse | None = None
