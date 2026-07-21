from typing import Optional
from pydantic import BaseModel


class IngestRequest(BaseModel):
    """Payload for ``POST /ingest`` — JSON strings or file uploads."""

    document: Optional[str] = None  # JSON string of document list
    question: Optional[str] = None  # JSON string of question→doc mapping
