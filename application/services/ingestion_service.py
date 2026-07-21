"""Use-case orchestrator for document / question ingestion."""

import json
import logging

from langchain_core.documents import Document

from application.dto.ingestion_dto import IngestionResult
from domain.ports.vector_store_port import VectorStorePort
from domain.services.chunking_service import chunk_docs

logger = logging.getLogger(__name__)


class IngestionService:
    """Orchestrate the ingestion of source documents and question mappings.

    Args:
        chunk_store: Vector store for document chunks.
        question_store: Vector store for question→document mappings.
    """

    def __init__(
        self,
        chunk_store: VectorStorePort,
        question_store: VectorStorePort,
    ) -> None:
        self._chunk_store = chunk_store
        self._question_store = question_store

    # ------------------------------------------------------------------
    def ingest_from_json_payloads(
        self,
        document_json: str | None,
        question_json: str | None,
    ) -> IngestionResult:
        """Ingest documents and/or questions from raw JSON strings.

        This mirrors the ``POST /ingest`` endpoint behaviour: each store is
        cleared before new data is loaded.
        """
        self._chunk_store.delete_all()
        self._question_store.delete_all()

        num_docs = 0
        num_questions = 0
        num_chunks = 0

        if document_json is not None:
            json_docs = json.loads(document_json)
            docs = [
                Document(metadata={"id": d["id"]}, page_content=d["text"])
                for d in json_docs
            ]
            chunked = chunk_docs(docs)
            self._chunk_store.add_documents(
                chunked,
                ids=[doc.metadata["chunk_id"] for doc in chunked],
            )
            num_docs = len(json_docs)
            num_chunks = len(chunked)
            logger.info(
                "Ingested %d documents → %d chunks.", num_docs, num_chunks
            )

        if question_json is not None:
            json_q = json.loads(question_json)
            q_docs = [
                Document(
                    metadata={"docs": json.dumps(d["docs"]), "id": d["id"]},
                    page_content=d["question"],
                )
                for d in json_q
            ]
            self._question_store.add_documents(
                q_docs,
                ids=[doc.metadata["id"] for doc in q_docs],
            )
            num_questions = len(json_q)
            logger.info("Ingested %d question mappings.", num_questions)

        return IngestionResult(
            num_documents=num_docs,
            num_questions=num_questions,
            num_chunks=num_chunks,
        )

    def ingest_from_files(
        self,
        docs_path: str,
        questions_path: str,
    ) -> IngestionResult:
        """Ingest from JSON files on disk.

        This mirrors the ``POST /ingest_file`` endpoint.
        """
        self._chunk_store.delete_all()
        self._question_store.delete_all()

        with open(docs_path, encoding="utf-8") as f:
            json_docs = json.load(f)
        with open(questions_path, encoding="utf-8") as f:
            json_q_mapping = json.load(f)

        doc_source = [
            Document(metadata={"id": d["id"]}, page_content=d["text"])
            for d in json_docs
        ]
        doc_question = [
            Document(
                metadata={"docs": json.dumps(d["docs"]), "id": d["id"]},
                page_content=d["question"],
            )
            for d in json_q_mapping
        ]

        # Chunk source documents
        chunked = chunk_docs(doc_source)
        self._chunk_store.add_documents(
            chunked,
            ids=[doc.metadata["chunk_id"] for doc in chunked],
        )

        # Store question mappings
        self._question_store.add_documents(
            doc_question,
            ids=[doc.metadata["id"] for doc in doc_question],
        )

        return IngestionResult(
            num_documents=len(json_docs),
            num_questions=len(json_q_mapping),
            num_chunks=len(chunked),
        )
