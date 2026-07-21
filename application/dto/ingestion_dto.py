"""DTOs for the document-ingestion use case."""

from dataclasses import dataclass


@dataclass
class IngestionResult:
    """Summary returned after a successful ingestion run."""

    num_documents: int = 0
    num_questions: int = 0
    num_chunks: int = 0
