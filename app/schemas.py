from pydantic import BaseModel


class IngestRequest(BaseModel):
    documents: list[str]


class AskRequest(BaseModel):
    question: str