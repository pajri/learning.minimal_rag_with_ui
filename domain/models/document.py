from dataclasses import dataclass, field


@dataclass
class ChunkMetadata:
    """Metadata for a single chunk derived from a source document."""

    doc_id: str = ""
    chunk_id: str = ""
    distance: float | None = None


@dataclass
class RetrievalResult:
    """A document retrieved from the vector store with its relevance score."""

    page_content: str
    metadata: dict = field(default_factory=dict)
    score: float = 0.0
