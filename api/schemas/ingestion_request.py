from pydantic import BaseModel

class DocumentRequest(BaseModel):
    id: str
    text: str

class QuestionRequest(BaseModel):
    id: str
    question: str
    docs: list[str]
    
class IngestRequest(BaseModel):
    document: DocumentRequest
    question: QuestionRequest