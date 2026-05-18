import json
import logging

from langchain_core.documents import Document
from application.common.pipeline.base_pipeline_step import BasePipelineStep
from application.config import DISTANCE_THRESHOLD
from application.rag.rag_pipeline_context import RagPipelineContext, RagPipelineErrorResponse


class ContextRetrievalStep(BasePipelineStep):
    def handle(self, rag_context: RagPipelineContext) :
        logger = logging.getLogger(__name__)
        
        # get data from context
        expanded_queries = rag_context.expanded_queries
        vectorstore_chunk = rag_context.vectorstore_chunk
        vectorstore_question = rag_context.vectorstore_question
        
        # get question-context mapping
        # context_result_question, _ = get_context_based_on_question_mapping(vectorstore_chunk, vectorstore_question, question)
        context_result_question = []
        
        # get context from vectorstore
        context_result = []
        for q in expanded_queries:
            _context_result = self.get_context_based_on_question(vectorstore_chunk, q)
            context_result.extend(_context_result)    

        logger.info(f"context_result_question: {context_result_question}")
        logger.info(f"context_result: {len(context_result)}")
        print(f"context_result: {len(context_result)}")

        # combine context from question-context mapping and context query
        contexts = [
            *(context_result_question or []),
            *(context_result or [])
        ]
        
        # remove duplicated context
        contexts = self.ensure_unique_context(contexts)
        print(f"unique context len: {len(contexts)}")

        # handle no context found
        if(len(contexts) == 0):
            rag_context.status = "error"
            rag_context.error_response = RagPipelineErrorResponse()
            rag_context.error_response.pipeline_name = "ContextRetrievalStep"
            rag_context.error_response.error_message = "No relevant context found for the question."
            return
        
        # context cleaning
        contexts = self.clean_filtered_context(contexts)

        # set result to context
        rag_context.documents = contexts
        self._next_handler.handle(rag_context)

    def clean_filtered_context(self, contexts):
        for c in contexts:
            if c.page_content.startswith(". "):
                c.page_content = c.page_content.lstrip(". ")

        return contexts

    def get_context_based_on_question_mapping(self, vectorstore_chunk, vectorstore_question, question):
        q_results = vectorstore_question.similarity_search_with_score(question, k=1)
        q_results = [q for q in q_results if q[1] < 0.4]

        doc_ids = []
        for doc, _ in q_results:
            doclist = json.loads(doc.metadata["docs"])
            doc_ids.extend(doclist)
        doc_ids = list(dict.fromkeys(doc_ids))

        if (len(doc_ids) == 0): return None, None
        
        doc_query_result = vectorstore_chunk._collection.get(
            where={"id": {"$in": doc_ids}}
        )

        if(doc_query_result is None): return None, None

        doc_result = [
            Document(page_content=doc, metadata=meta)
            for doc, meta in zip(doc_query_result["documents"], doc_query_result["metadatas"])
        ]

        return doc_result, q_results

    def get_context_based_on_question(self, vectorstore_chunk, question):
        contexts = vectorstore_chunk.similarity_search_with_score(question, k=3)
        contexts = self.filter(contexts)

        return contexts

    def ensure_unique_context(self, contexts):
        seen = set()
        unique_contexts = []

        for doc in contexts:
            content = doc.page_content.strip()
            
            if content not in seen:
                seen.add(content)
                unique_contexts.append(doc)

        contexts = unique_contexts
        return contexts
    
    def filter(self, documents):
        approved_chunks = []
        for doc, score in documents:
            if score <= DISTANCE_THRESHOLD:
                doc.metadata["distance"] = score
                approved_chunks.append(doc)
            
        approved_chunks.sort(key=lambda d: d.metadata["distance"])  

        return approved_chunks