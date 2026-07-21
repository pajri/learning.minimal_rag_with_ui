"""HTTP route handlers — thin controllers.

All business logic is delegated to application services injected via
FastAPI's dependency-injection system (see :mod:`api.dependencies`).
"""

import logging

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from api import constants
from api.dependencies import (
    get_filtering_service,
    get_ingestion_service,
    get_rag_service,
    get_vectorstore_chunk,
    get_vectorstore_question,
)
from api.schemas import ApiResponse, AskRequest, AskResponse, IngestRequest, SourceDocumentResponse
from application.dto.filtering_dto import FilterDecision
from application.services.filtering_service import FilteringService
from application.services.ingestion_service import IngestionService
from application.services.rag_service import RagService
from domain.ports.vector_store_port import VectorStorePort

router = APIRouter()
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Ingestion
# ---------------------------------------------------------------------------


@router.post("/ingest")
def ingest(
    req: IngestRequest,
    ingestion_service: IngestionService = Depends(get_ingestion_service),
):
    result = ingestion_service.ingest_from_json_payloads(
        document_json=req.document,
        question_json=req.question,
    )
    return ApiResponse(
        success=True,
        message=constants.INGESTION_COMPLETED_MESSAGE,
        data={
            "num_documents": result.num_documents,
            "num_questions": result.num_questions,
            "num_chunks": result.num_chunks,
        },
    )


@router.post("/ingest_file")
def ingest_file(
    ingestion_service: IngestionService = Depends(get_ingestion_service),
):
    from infrastructure.config import settings

    docs_path = str(settings.base_dir / "dataset" / "machine_learning_knowledge.json")
    questions_path = str(
        settings.base_dir / "dataset" / "machine_learning_knowledge_question_doc_mapping.json"
    )

    result = ingestion_service.ingest_from_files(
        docs_path=docs_path,
        questions_path=questions_path,
    )
    return ApiResponse(
        success=True,
        message=constants.INGESTION_COMPLETED_MESSAGE,
        data={
            "num_documents": result.num_documents,
            "num_questions": result.num_questions,
            "num_chunks": result.num_chunks,
        },
    )


# ---------------------------------------------------------------------------
# Ask
# ---------------------------------------------------------------------------


@router.post("/ask")
def ask(
    req: AskRequest,
    rag_service: RagService = Depends(get_rag_service),
    filtering_service: FilteringService = Depends(get_filtering_service),
):
    logger.info("POST /ask — question: %s", req.question[:80])

    # ---- input filtering ----------------------------------------------------
    outcome = filtering_service.check_input(req.question)

    if outcome.decision == FilterDecision.SAFE_RESPONSE:
        logger.info("Input triggered safe response for: %s", outcome.reason)
        return ApiResponse(
            success=True,
            message=constants.ANSWER_GENERATED_MESSAGE,
            data=AskResponse(
                question=req.question,
                answer=outcome.safe_message,
                source_documents=[],
            ),
        )

    if outcome.decision == FilterDecision.REJECT:
        logger.info("Input rejected: %s", outcome.reason)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ApiResponse(
                success=False,
                message=constants.INVALID_INPUT_MESSAGE,
                data=None,
                error=outcome.reason,
            ).model_dump(),
        )

    # ---- RAG pipeline -------------------------------------------------------
    logger.info("Input valid, running RAG pipeline …")
    question = outcome.filtered_text
    rag_result = rag_service.ask(question)

    logger.info("RAG pipeline finished. answer=%s", rag_result.answer[:80])

    if not rag_result.has_answer:
        return ApiResponse(
            success=True,
            message=constants.ANSWER_GENERATED_MESSAGE,
            data=AskResponse(
                question=req.question,
                answer="I do not know the answer based on the provided context.",
                source_documents=[],
            ),
        )

    # ---- output filtering ---------------------------------------------------
    output_outcome = filtering_service.check_output(
        rag_result.answer, rag_result.source_documents
    )
    if not output_outcome.valid:
        logger.info("Output rejected: %s", output_outcome.reason)
        return ApiResponse(
            success=True,
            message=f"{constants.OUTPUT_FILTERING_FAILED_MESSAGE} {output_outcome.reason}",
            data=AskResponse(
                question=req.question,
                answer=constants.OUTPUT_FILTERING_FAILED_ANSWER,
                source_documents=[],
            ),
        )

    # ---- success ------------------------------------------------------------
    source_docs = [
        SourceDocumentResponse(
            page_content=doc.page_content, metadata=doc.metadata
        )
        for doc in rag_result.source_documents
    ]
    return ApiResponse(
        success=True,
        message=constants.ANSWER_GENERATED_MESSAGE,
        data=AskResponse(
            question=req.question,
            answer=rag_result.answer,
            source_documents=source_docs,
        ),
    )
