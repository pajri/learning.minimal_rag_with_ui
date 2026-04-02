from pydantic import BaseModel

class SourceDocumentResponse(BaseModel):
    page_content: str
    metadata: dict
    
class AskResponse(BaseModel):
    question: str
    answer: str
    source_documents: list[SourceDocumentResponse]

