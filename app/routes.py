from fastapi import APIRouter
from app.schemas import IngestRequest, AskRequest
from .rag.pipeline import rag_pipeline
from .ingestion.pipeline import ingestion_pipeline

router = APIRouter()

collection = None  # will be injected from main


def set_collection(col):
    global collection
    collection = col


@router.post("/ingest")
def ingest(req: IngestRequest):
    docs = ingestion_pipeline(req.documents)

    return {"status": "ok", "num_documents": len(docs)}


@router.post("/ask")
def ask(req: AskRequest):
    question = req.question
    answer = rag_pipeline(question)
    if answer is None:
        return {
            "question": req.question,
            "results": "I do not know the answer based on the provided context."
        }
    
    return {
        "question": req.question,
        "results": answer
    }

    