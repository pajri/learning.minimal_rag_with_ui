import logging

from fastapi import APIRouter, Depends
from schemas import IngestRequest, AskRequest
from .rag.pipeline import rag_pipeline
from .ingestion.pipeline import ingestion_pipeline
from .dependencies import get_collection

router = APIRouter()
logger = logging.getLogger()

@router.post("/ingest")
def ingest(req: IngestRequest, collection=Depends(get_collection)):
    docs = ingestion_pipeline(req.documents, collection)

    return {"status": "ok", "num_documents": len(docs)}


@router.post("/ask")
def ask(req: AskRequest, collection = Depends(get_collection)):
    logger.info("start /ask")
    question = req.question
    answer, documents = rag_pipeline(question, collection)
    if answer is None:
        logger.info("done /ask. no answer provided")
        return {
            "question": req.question,
            "results": "I do not know the answer based on the provided context."
        }
    
    logger.info("done /ask")
    return {
        "question": req.question,
        "answer": answer,
        "sources": documents
    }

    