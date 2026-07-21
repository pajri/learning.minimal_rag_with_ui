"""DTOs for the RAG ask use case."""

from dataclasses import dataclass, field

from langchain_core.documents import Document


@dataclass
class RagResult:
    """The full result of running the RAG pipeline."""

    question: str
    answer: str
    source_documents: list[Document] = field(default_factory=list)
    system_prompt: str = ""
    user_prompt: str = ""

    @property
    def has_answer(self) -> bool:
        return bool(self.answer)
