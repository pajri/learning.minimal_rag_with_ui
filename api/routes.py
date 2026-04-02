import logging
import json

from api import constants
from api.schemas import IngestRequest, AskRequest, ApiResponse, AskResponse, SourceDocumentResponse  
from api.util import get_vectorstore_chunk, get_vectorstore_question

from application.rag.pipeline import rag_pipeline
from application.ingestion.pipeline import chunk_ingestion_pipeline, question_ingestion_pipeline
from application.storage.setup import delete_all_docs
from application.filtering import input_filtering, output_filtering
from application.config import BASE_DIR

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

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

    api_response = ApiResponse(
        success=True,
        message=constants.INGESTION_COMPLETED_MESSAGE,
        data={"num_documents": len(doc_source), "num_questions": len(doc_question)}
    )
    return api_response

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
    api_response = ApiResponse(
        success=True,
        message=constants.INGESTION_COMPLETED_MESSAGE,
        data={"num_documents": len(doc_source), "num_questions": len(doc_question)}
    )
    return api_response
# endregion


@router.post("/ask")
def ask(req: AskRequest, vectorstore_chunk = Depends(get_vectorstore_chunk), vectorstore_question = Depends(get_vectorstore_question)):
    logger.info("start /ask")
    logger.info(f"question: {req.question}")

    response_api = None

    """
    TODO: i think we can try to separate between input filtering and input validation.
    input filtering is to filter unsafe content (e.g. self-harm, kill, bomb, etc.).
        when input filtering failed, we can still return 200 with a safe answer 
        (e.g. for self-harm, we can return a message to seek help from trusted people or mental health professionals). 

    input validation is to filter input that is harmful to the system (e.g. prompt injection, sql injection, etc.). 
        this also includes validating the format of the input (e.g. maxlength).
        when input validation failed, we can return 400 with an error message.
    """
    valid, result = input_filtering.filter(req.question)
    logger.info(f"after input filtering, valid: {valid}, result: {result}")

    if not valid:
        print('invalid input detected')
        logger.info("done /ask. input not valid")

        
        if "self-harm" in result.lower():
            response_api = ApiResponse(
                success=True,
                message=constants.ANSWER_GENERATED_MESSAGE,
                data=AskResponse(
                    question=req.question,
                    answer=constants.SELF_HARM_ANSWER,
                    source_documents=[]
                )
            )
        else:
            response_api = JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=ApiResponse(
                    success=False,
                    message=constants.INVALID_INPUT_MESSAGE,
                    data=None,
                    error = result
                ).model_dump()
            )
    
        return response_api
    
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
        response_api = ApiResponse(
            success=True,
            message=constants.ANSWER_GENERATED_MESSAGE,
            data=AskResponse(
                question=req.question,
                answer="I do not know the answer based on the provided context.",
                source_documents=[]
            )
        )
        return response_api
    

    valid, result = output_filtering.filter(answer, contexts)
    if not valid:
        print('output not valid')
        logger.info("done /ask. output not valid")

        api_response = ApiResponse(
            success=True,
            message=f"constants.OUTPUT_FILTERING_FAILED_MESSAGE {result}",
            data=AskResponse(
                question=req.question,
                answer=constants.OUTPUT_FILTERING_FAILED_ANSWER,
                source_documents=[]
            )

        )   

        return api_response
    
    logger.info("done /ask")

    
    source_documents = [SourceDocumentResponse(page_content=doc.page_content, metadata=doc.metadata) for doc in contexts]
    data = AskResponse(question=req.question, answer=answer, source_documents=source_documents)
    response_api = ApiResponse(
        success=True,
        message=constants.ANSWER_GENERATED_MESSAGE,
        data=data
    )

    return response_api
    