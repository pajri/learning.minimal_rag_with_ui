from fastapi import APIRouter, Depends
from app.schemas import IngestRequest, AskRequest
from .rag.pipeline import rag_pipeline
from .ingestion.pipeline import ingestion_pipeline
from .dependencies import get_collection

router = APIRouter()

collection = None  # will be injected from main


def set_collection(col):
    global collection
    collection = col


@router.post("/ingest")
def ingest(req: IngestRequest, collection=Depends(get_collection)):
    docs = ingestion_pipeline(req.documents, collection)

    return {"status": "ok", "num_documents": len(docs)}


@router.post("/ask")
def ask(req: AskRequest, collection = Depends(get_collection)):
    question = req.question
    answer = rag_pipeline(question, collection)
    if answer is None:
        return {
            "question": req.question,
            "results": "I do not know the answer based on the provided context."
        }
    
    return {
        "question": req.question,
        "results": answer
    }

    