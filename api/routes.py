import logging
import json

from api.schemas import IngestRequest, AskRequest
from api.util import get_vectorstore_chunk, get_vectorstore_question

from application.rag.pipeline import rag_pipeline
from application.ingestion.pipeline import chunk_ingestion_pipeline, question_ingestion_pipeline
from application.storage.setup import delete_all_docs
from application.filtering import input_filtering, output_filtering
from application.config import BASE_DIR

from fastapi import APIRouter, Depends

from langchain_core.documents import Document


router = APIRouter()
logger = logging.getLogger()

# region ingestion
@router.post("/ingest")
def ingest(req: IngestRequest):
    vectorstore_chunk = get_vectorstore_chunk(req)
    vectorstore_question = get_vectorstore_question(req)
    
    delete_all_docs(vectorstore_chunk)
    delete_all_docs(vectorstore_question)

    doc_source = []
    doc_question = []

    if req.document is not None:
        json_docs = json.load(req.document)
        doc_source = [Document(metadata={"id": doc["id"]}, page_content=doc["text"]) for doc in json_docs]
        chunk_ingestion_pipeline(vectorstore_chunk, doc_source)


    if req.question is not None:
        json_question_doc_mapping = json.load(req.question)
        doc_question =[Document(metadata={"docs": json.dumps(doc["docs"]), "id":doc["id"]}, page_content=doc["question"]) for doc in json_question_doc_mapping]
        question_ingestion_pipeline(vectorstore_question, doc_question)

    return {"status": "ok", "num_documents": len(doc_source) + len(doc_question)}

@router.post("/ingest_file")
def ingest(vectorstore_chunk = Depends(get_vectorstore_chunk), vectorstore_question = Depends(get_vectorstore_question)):
    # regresh collection
    delete_all_docs(vectorstore_chunk)
    delete_all_docs(vectorstore_question)

    # load files
    with open(f"{BASE_DIR}/dataset/machine_learning_knowledge.json") as f:
        json_docs = json.load(f)
        print(f"docs: {json_docs[0]}")

    with open(f"{BASE_DIR}/dataset/machine_learning_knowledge_question_doc_mapping.json") as f:
        json_question_doc_mapping = json.load(f)
        print(f"docs_question: {json_question_doc_mapping[0]}")

    # populate documents
    doc_source = [Document(metadata={"id": doc["id"]}, page_content=doc["text"]) for doc in json_docs]
    doc_question = [Document(metadata={"docs": json.dumps(doc["docs"]), "id":doc["id"]}, page_content=doc["question"]) for doc in json_question_doc_mapping]

    # process ingestion
    question_ingestion_pipeline(vectorstore_question, doc_question)
    chunk_ingestion_pipeline(vectorstore_chunk, doc_source)

    # return result
    return {"status": "ok", "num_documents": len(doc_source), "num_questions": len(doc_question)}
# endregion


@router.post("/ask")
def ask(req: AskRequest, vectorstore_chunk = Depends(get_vectorstore_chunk), vectorstore_question = Depends(get_vectorstore_question)):
    logger.info("start /ask")
    logger.info(f"question: {req.question}")

    valid, result = input_filtering.filter(req.question)
    logger.info(f"after input filtering, valid: {valid}, result: {result}")

    if not valid:
        print('invalid input detected')
        logger.info("done /ask. input not valid")
        return {
            "question": req.question,
            "results": result
        }
    
    print('input valid, proceed to rag pipeline')
    question = result
    answer, contexts, system_prompt, user_prompt = rag_pipeline(vectorstore_chunk, vectorstore_question, question)

    logger.info(f"rag_pipeline finished")
    logger.info(f"answer: {answer}")
    logger.info(f"retrieved contexts: {contexts}")
    logger.info(f"system_prompt: {system_prompt}")
    logger.info(f"user_prompt: {user_prompt}")

    if answer is None:
        logger.info("done /ask. no answer provided")
        return {
            "question": req.question,
            "results": "I do not know the answer based on the provided context."
        }
    

    valid, result =output_filtering.filter(answer, contexts)
    if not valid:
        print('output not valid')
        logger.info("done /ask. output not valid")
        return {
            "question": req.question,
            "results": result
        }
    
    logger.info("done /ask")
    return {
        "question": req.question,
        "answer": answer,
        "sources": contexts
    }
    