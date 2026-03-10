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

class DocumentResult():
    def __init__(self, id: str, content: str, distance: float):
        self.id = id
        self.content = content
        self.distance = distance
