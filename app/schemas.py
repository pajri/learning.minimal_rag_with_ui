from pydantic import BaseModel

### request model ###
class IngestRequest(BaseModel):
    documents: list[str]

    

class AskRequest(BaseModel):
    question: str

### dto schemas ###
class Document():
    def __init__(self, id: str, content: str):
        self.id = id
        self.content = content

class DocumentResult(Document):
    def __init__(self, id: str, content: str, distance: float):
        super().__init__(id, content)
        self.distance = distance

class DocumentEval():
    def __init__(self, question: str, answer: str, relevant_doc_ids: list):
        self.question = question
        self.answer = answer
        self.relevant_doc_ids = relevant_doc_ids